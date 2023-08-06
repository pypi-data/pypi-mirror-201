#include "weights.h"

#include <random>
#include <algorithm>
#include <cmath>
#include <numeric>

#include <boost/math/quadrature/tanh_sinh.hpp>
#include <boost/math/special_functions/pow.hpp>

template<int N>
static std::pair<Pixel<float, N>,Pixel<float, N>> sample_aggregate_neighborhood(const Image<float, N>& aggregateHorizontal, const Image<float, N>& aggregateVertical, Eigen::Vector2i p1, Eigen::Vector2i p2, int filter_size_parallel, int filter_size_orthogonal) {
    Eigen::Vector2i p1sum;
    Eigen::Vector2i p2sum;
    const Image<float,N>* sum;
    if(p1[0] == p2[0]) {
        // horizontal case, i.e.:
        // *  *   *   *
        // *  p2  p1  *
        // *  *   *   *
        p1sum[0] = p1[0] - filter_size_orthogonal/2;
        p1sum[1] = p1[1];
        p2sum[0] = p2[0] - filter_size_orthogonal/2;
        p2sum[1] = p2[1] - filter_size_parallel;
        sum = &aggregateHorizontal;

        assert(p2[1] < p1[1]);
    } else {
        // vertical case, i.e.:
        // *  *   *
        // *  p2  *
        // *  p1  *
        // *  *   *
        p1sum[0] = p1[0];
        p1sum[1] = p1[1] - filter_size_orthogonal/2;
        p2sum[0] = p2[0] - filter_size_parallel;
        p2sum[1] = p2[1] - filter_size_orthogonal/2;
        sum = &aggregateVertical;

        assert(p2[0] < p1[0]);
    }
    p1sum[0] = std::clamp(p1sum[0], 0, (int)sum->rows()-1);
    p1sum[1] = std::clamp(p1sum[1], 0, (int)sum->cols()-1);
    p2sum[0] = std::clamp(p2sum[0], 0, (int)sum->rows()-1);
    p2sum[1] = std::clamp(p2sum[1], 0, (int)sum->cols()-1);

    return sample(*sum, p1sum, p2sum);
}


float GlobalGaussianParameterBian::weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const {
    auto [v1, v2] = sample(mean, p1, p2);
    float diff = v1[0]-v2[0];
    float diffsq = diff*diff;

    float w = std::exp(-diffsq/(2.0f*variance));
    //float minweight = 1e-5;
    //return std::max(w, minweight);
    return w;
}

GlobalGaussianParameterBian::GlobalGaussianParameterBian(const Image<float, 1>& img, int filter_s)
    : mean()
    , variance()
{
    int blur_size = size(filter_s);

#if 1
    //Mean
    mean = meanFilterClamped<float, 1>(img, filter_s, filter_s);
    float difference_factor = 2.0f/(blur_size*blur_size*blur_size);
#else
    //Median
    mean = medianFilter<filter_s,filter_s>(img);
    float difference_factor;
    switch (filter_s) {
        case 1:
            difference_factor = 0.142;
            break;
        case 2:
            difference_factor = 0.030;
            break;
        default:
            assert(false);
            break;
    }
#endif

    int rows = mean.rows();
    int cols = mean.cols();

    float sum_of_differences = 0.0f;

    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            float o = img(y,x)[0];
            float m = mean(y,x)[0];
            float diff = o-m;

            sum_of_differences += blur_correction_factor(filter_s, filter_s) * diff * diff;
        }
    }

    int num_voxels = rows * cols;
    float uncorrected_variance = sum_of_differences/num_voxels;

    variance =  difference_factor * uncorrected_variance;
}


static float bayesBhattacharyyaPoisson(float sum1, float sum2) {
    // Guesswork approximation using p(x|l)
    //float diff = std::sqrt(sum1)-std::sqrt(sum2);
    //float diffsq = diff*diff;
    //float w = std::exp(-diffsq*0.5f);

    float exponent = std::lgamma((sum1+sum2+2.0f)*0.5f) - (std::lgamma(sum1+1) + std::lgamma(sum2+1))*0.5f;
    float w = std::exp(exponent);
    return w;
}

PoissonParameter::PoissonParameter(const Image<float, 1>& img, int search_extent, int filter_extent)
    : img(img)
    , estimatedParams()
    , filter_extent(filter_extent)
    , search_extent(search_extent)
{
    estimatedParams = meanFilterClamped<float, 1>(img, filter_extent, filter_extent);
}

float PoissonParameter::weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const {
    auto poissonSimilarity = [] (const Image<float, 1>& img, std::vector<Eigen::Vector2i> neighborhood1, std::vector<Eigen::Vector2i> neighborhood2) {
        if(neighborhood1.size() > neighborhood2.size()) {
            neighborhood1.resize(neighborhood2.size());
        } else if(neighborhood1.size() < neighborhood2.size()) {
            neighborhood2.resize(neighborhood1.size());
        }
        assert(neighborhood1.size() == neighborhood2.size());

        auto sum = [&] (const std::vector<Eigen::Vector2i>& vals) -> float {

            float sum = 0.0f;
            for(const auto& p : vals) {
                sum += sample<float, 1>(img, p)[0];
            }
            return sum;
        };

        float sum1 = sum(neighborhood1);
        float sum2 = sum(neighborhood2);

        float w = bayesBhattacharyyaPoisson(sum1, sum2);


        assert(!std::isnan(w) && std::isfinite(w) && w >= 0);

        return w;
    };

    auto probForParamsGivenSample = [] (Pixel<float, 1> lambda, Pixel<float, 1> sample) -> float {
        float exponent = -lambda[0] + std::log(lambda[0]) * sample[0] - std::lgamma(sample[0] + 1);
        return std::exp(exponent);
    };

    return dynamic_neighborhood_similarity(poissonSimilarity, probForParamsGivenSample, img, estimatedParams, search_extent, filter_extent, p1, p2);
}

LoupasParameter::LoupasParameter(const Image<float, 1>& img, int search_extent, int filter_extent)
    : img(img)
    , estimatedParams()
    , filter_extent(filter_extent)
    , search_extent(search_extent)
    , sigma2()
{
    Image<float, 1> mean = meanFilterClamped(img, filter_extent, filter_extent);
    Image<float, 1> variance = variances(img, mean, filter_extent, filter_extent);

    //Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic> sigma2s = variance.binaryExpr(mean, [](Pixel<float,1> v, Pixel<float,1> m){ return v[0]/m[0]; });
    //sigma2 = sigma2s.mean();

    int rows = img.rows();
    int cols = img.cols();
    std::vector<float> vals;
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            vals.push_back(variance(y,x)[0] / mean(y,x)[0]);
        }
    }
    size_t mid = vals.size()/2;
    std::nth_element(vals.begin(), vals.begin()+mid, vals.end());
    float median = vals[mid];
    //TODO: good results seem to be REALLY dependent on good parameter estimation... is there a better way?
    sigma2 = median;

    // TODO maybe a median filter would also make sense here?
    // it seems to produce really bad results, though...
    estimatedParams = mean;
}

// The integral-part of the expression for the modified bessel function of 2nd order (K_v(x))
// References:
// https://math.stackexchange.com/questions/1960778/approximating-the-log-of-the-modified-bessel-function-of-the-second-kind
// https://onlinelibrary.wiley.com/templates/jsp/_ux3/_acropolis/_pericles/pdf-viewer/web/viewer.html?file=/doi/pdfdirect/10.1002/cnm.972
static double bessel_K_integral_log(double v, double x) {
    // double seems to be fine here, float does not have enough exponent bits.
    // long double also works, but requires considerably more computation time
    typedef double Float;
    if (v==0.5f) {
        return 0.0f;
    }
    v = std::abs(v);
    assert(v < 50); //Loupas method becomes numerically unstable for too large neighborhood sizes. :(
    constexpr size_t n = 8;
    Float beta = (2*n) / (2.0f * v + 1.0f);

    Float v_minus_05 = v-0.5;
    Float v_exp_2 = -2.0 * v -1.0;

    Float error;
    Float L1;
    size_t levels;
    //Float termination = 0.01;
    Float termination = std::sqrt(std::numeric_limits<Float>::epsilon());

    boost::math::quadrature::tanh_sinh<Float> integrator;
    Float res = integrator.integrate([&](const Float u) {
        auto u_power_beta = std::pow(u, beta);
        auto first = beta * std::exp(-u_power_beta) * std::pow(2.0 * x + u_power_beta, v_minus_05) * boost::math::pow<n-1>(u);
        auto second = std::exp(-1.0 / u);
        if (second > 0) {
            second *= std::pow(u, v_exp_2) * std::pow(2 * x * u + 1, v_minus_05);
        }
        return first + second;
    }, 0.0, 1.0, termination, &error, &L1, &levels);

    return std::log(res);
}


float LoupasParameter::weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const {
    auto similarity = [this] (const Image<float, 1>& img, std::vector<Eigen::Vector2i> neighborhood1, std::vector<Eigen::Vector2i> neighborhood2) {
        if(neighborhood1.size() > neighborhood2.size()) {
            neighborhood1.resize(neighborhood2.size());
        } else if(neighborhood1.size() < neighborhood2.size()) {
            neighborhood2.resize(neighborhood1.size());
        }
        assert(neighborhood1.size() == neighborhood2.size());

        auto sum_sq = [&] (const std::vector<Eigen::Vector2i>& vals) -> float {
            float sum = 0.0f;
            for(const auto& p : vals) {
                float s = sample<float, 1>(img, p)[0];
                sum += s*s;
            }
            return sum;
        };
        float n = neighborhood1.size();
        float v = (-n*0.5+1);

        float Ex2 = sum_sq(neighborhood1)/n;
        float Ey2 = sum_sq(neighborhood2)/n;
        float Ez2 = (Ex2 + Ey2)*0.5f;

        float nfactor = n/(2.0f*sigma2);
        float expf1 = nfactor * ((std::sqrt(Ex2) + std::sqrt(Ey2))*0.5f - std::sqrt(Ez2));

        float dx = std::sqrt(Ex2) * nfactor;
        float dy = std::sqrt(Ey2) * nfactor;
        float dz = std::sqrt(Ez2) * nfactor;

        double intx_log = bessel_K_integral_log(v, dx);
        double inty_log = bessel_K_integral_log(v, dy);
        double intz_log = bessel_K_integral_log(v, dz);

        double expf2 = intz_log - (intx_log + inty_log)*0.5f;

        double w = std::exp(expf1 + expf2);

        //w = std::min(w, 1.0f);
        assert(!std::isnan(w) && std::isfinite(w) && 0 <= w && w <= 1.1);

        return w;
    };

    auto probForParamsGivenSample = [this] (Pixel<float, 1> mu_p, Pixel<float, 1> sample_p) -> float {
        float mu = mu_p[0];
        float sample = sample_p[0];
        auto diff = mu-sample;
        auto diffSq = diff*diff;

        float e = std::exp(-diffSq/(2*mu*sigma2));
        float f = 1/std::sqrt(2.0f * M_PI * mu * sigma2);

        float w = f*e;

        return w;
    };

    return dynamic_neighborhood_similarity(similarity, probForParamsGivenSample, img, estimatedParams, search_extent, filter_extent, p1, p2);
}


TTestParameter::TTestParameter(const Image<float, 1>& img, int search_extent, int filter_extent)
    : img(img)
    , estimatedParams(img.rows(), img.cols())
    , search_extent(search_extent)
    , filter_extent(filter_extent)
{
    Image<float, 1> mean = meanFilterClamped(img, filter_extent, filter_extent);
    Image<float, 1> variance = variances(img, mean, filter_extent, filter_extent);

    int rows = img.rows();
    int cols = img.cols();
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            estimatedParams(y,x) = { mean(y,x)[0], variance(y,x)[0] };
        }
    }

}

static std::vector<float> sample_vals(const Image<float, 1>& img, const std::vector<Eigen::Vector2i> ps) {
    std::vector<float> result;
    std::transform(ps.begin(), ps.end(), std::back_inserter(result), [&](auto p) {return sample(img, p)[0];});

    return result;
};
static std::pair<float, float> mean_and_var(const std::vector<float>& vals) {
    float sum = 0.0f;
    for(const auto& p : vals) {
        sum += p;
    }
    float mean = sum/vals.size();

    float sq_sum = 0.0f;
    for(const auto& p : vals) {
        sq_sum += square(mean-p);
    }
    float variance = sq_sum/(vals.size()-1);

    return {mean, variance};
};

float TTestParameter::weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const {
    auto tDistributionSimilarity = [] (const Image<float, 1>& img, std::vector<Eigen::Vector2i> neighborhood1, std::vector<Eigen::Vector2i> neighborhood2) {

        auto v1 = sample_vals(img, neighborhood1);
        auto v2 = sample_vals(img, neighborhood2);

        auto [mean1, var1] = mean_and_var(v1);
        auto [mean2, var2] = mean_and_var(v2);

        float n1 = neighborhood1.size();
        float n2 = neighborhood2.size();

        float sn1 = var1/n1;
        float sn2 = var2/n2;

        float T_square;
        if(mean1 == mean2) {
            T_square = 0.0;
        } else {
            T_square = square(mean1 - mean2)/(sn1 + sn2);
        }

        float m_star;
        if(var1==0 && var2==0) {
            m_star = square(1.0f/n1 + 1.0f/n2)/(1.0f/(square(n1)*(n1-1.0f)) + 1.0f/(square(n2)*(n2-1.0f)));
        } else {
            m_star = square(sn1+sn2)/(square(sn1)/(n1-1.0f) + square(sn2)/(n2-1.0f));
        }

        float m = std::round(m_star);

        float tpow = std::pow(1.0f+T_square/m, -0.5f*(m+1.0f));
        assert(!std::isnan(tpow) && std::isfinite(tpow));

        //float gamma1 = tgamma((m+1.0f)*0.5f);
        //float gamma2 = tgamma(m*0.5f);

        //assert(!std::isnan(gamma1) && std::isfinite(gamma1));
        //assert(!std::isnan(gamma2) && std::isfinite(gamma2));

        //float w = gamma1/(std::sqrt(m)*gamma2*tpow);

        //The above sucks if m is too large, so we express the t-distribution pdf using the beta function
        float beta_term = std::betaf(0.5f, m*0.5f);
        assert(!std::isnan(beta_term) && std::isfinite(beta_term) && beta_term > 0);

        float w = tpow/(std::sqrt(m)*beta_term);


        assert(!std::isnan(w) && std::isfinite(w) && w >= 0);

        return w;
    };

    return dynamic_neighborhood_similarity(tDistributionSimilarity, gaussian_pdf, img, estimatedParams, search_extent, filter_extent, p1, p2);
}

VariableGaussianParameter::VariableGaussianParameter(const Image<float, 1>& img, int search_extent, int filter_extent)
    : img(img)
    , estimatedParams(img.rows(), img.cols())
    , search_extent(search_extent)
    , filter_extent(filter_extent)
{
    Image<float, 1> mean = meanFilterClamped(img, filter_extent, filter_extent);
    Image<float, 1> variance = variances(img, mean, filter_extent, filter_extent);

    int rows = img.rows();
    int cols = img.cols();
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            estimatedParams(y,x) = { mean(y,x)[0], variance(y,x)[0] };
        }
    }

}

float VariableGaussianParameter::weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const {
    auto variableGaussianSimilarity = [] (const Image<float, 1>& img, std::vector<Eigen::Vector2i> neighborhood1, std::vector<Eigen::Vector2i> neighborhood2) {
        if(neighborhood1.size() > neighborhood2.size()) {
            neighborhood1.resize(neighborhood2.size());
        } else if(neighborhood1.size() < neighborhood2.size()) {
            neighborhood2.resize(neighborhood1.size());
        }
        size_t n = neighborhood1.size();
        assert(n == neighborhood2.size());

        auto v1 = sample_vals(img, neighborhood1);
        auto v2 = sample_vals(img, neighborhood2);

        auto [mean1, var1] = mean_and_var(v1);
        auto [mean2, var2] = mean_and_var(v2);

        float nom = std::sqrt(var1*var2);
        float denom = (var1+var2)*0.5 + square((mean1-mean2)*0.5);

        if(denom == 0.0f) {
            return 1.0f;
        }

        float quotient = nom/denom;

        assert(n>=4);
        float exponent = (n-3.0)/2;
        float w = std::pow(quotient, exponent);


        assert(!std::isnan(w) && std::isfinite(w) && w >= 0);

        return w;
    };

    return dynamic_neighborhood_similarity(variableGaussianSimilarity, gaussian_pdf, img, estimatedParams, search_extent, filter_extent, p1, p2);
}
