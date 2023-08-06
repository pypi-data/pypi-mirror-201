#pragma once
#include "imgs.h"

struct Parameters {
    virtual ~Parameters() {};
    virtual float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const = 0;
};

template<int N>
struct ManualParameter : public Parameters {
    Image<float, N> img;

    float beta;

    ManualParameter(const Image<float, N>& img, float beta);

    float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const;
};

template<int N>
struct GlobalGaussianParameterGeneric : public Parameters {
    typedef Eigen::Matrix<float, N, N> Matrix;

    Image<float, N> img;
    Image<float, N> estimatedParams;
    Matrix covariance_inv;
    int search_extent;
    int filter_extent;

    GlobalGaussianParameterGeneric(const Image<float, N>& img, int search_extent, int filter_extent);

    float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const;
};

struct GlobalGaussianParameterBian : public Parameters {
    Image<float, 1UL> mean;
    float variance;
    int filter_extent;
    GlobalGaussianParameterBian(const Image<float, 1>& img, int filter_extent);

    float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const;
};

struct GaussianParameters {
    float mean;
    float variance;
};
struct TTestParameter : public Parameters {
    const Image<float, 1>& img;
    Eigen::Matrix<GaussianParameters, Eigen::Dynamic, Eigen::Dynamic> estimatedParams;
    TTestParameter(const Image<float, 1>& img, int search_extent, int filter_extent);
    int search_extent;
    int filter_extent;

    float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const;
};

struct VariableGaussianParameter : public Parameters {
    const Image<float, 1>& img;
    Eigen::Matrix<GaussianParameters, Eigen::Dynamic, Eigen::Dynamic> estimatedParams;
    VariableGaussianParameter(const Image<float, 1>& img, int search_extent, int filter_extent);
    int search_extent;
    int filter_extent;

    float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const;
};

struct PoissonParameter : public Parameters {
    const Image<float, 1>& img;
    Image<float, 1> estimatedParams;
    int filter_extent;
    int search_extent;

    PoissonParameter(const Image<float, 1>& img, int search_extent, int filter_extent);
    float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const;
};

struct LoupasParameter : public Parameters {
    const Image<float, 1>& img;
    Image<float, 1> estimatedParams;
    int filter_extent;
    int search_extent;
    float sigma2;

    LoupasParameter(const Image<float, 1>& img, int search_extent, int filter_extent);
    float weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const;
};

/// ----------------------------------------------------------------------------
/// Implementation -------------------------------------------------------------
/// ----------------------------------------------------------------------------

inline long linear_order(const Eigen::Vector2i& p) {
    return long(p(1)) + (long(p(0)) << 32);
}

inline bool cmp_linear(const Eigen::Vector2i& p1, const Eigen::Vector2i& p2) {
    return linear_order(p1) < linear_order(p2);
}

inline float square(float s) {
    return s*s;
}

inline int dist_sq(const Eigen::Vector2i& p1, const Eigen::Vector2i& p2) {
    return square(p1(0)-p2(0)) + square(p1(1)-p2(1));
}

inline float gaussian_pdf_exp(float val, float mean, float variance) {
    return std::exp(-0.5f/variance * square(val-mean));
}

inline float gaussian_pdf(GaussianParameters params, Pixel<float,1> val) {
    return gaussian_pdf_exp(val[0], params.mean, params.variance)/std::sqrt(2.0f * 3.141592654f* params.variance);
}

template<typename ProbForParamsGivenSample, typename P, int N>
Eigen::Vector2i best_neighborhood(ProbForParamsGivenSample probForParamsGivenSample, const Image<float, N>& img, const Eigen::Matrix<P, Eigen::Dynamic, Eigen::Dynamic>& params, Eigen::Vector2i samplePoint, Eigen::Vector2i center, Eigen::Vector2i filter_size) {
    int rows = img.rows();
    int cols = img.cols();

    assert(params.rows() == rows);
    assert(params.cols() == cols);

    int xbase = std::clamp(center(1), 0, cols-1);
    int ybase = std::clamp(center(0), 0, rows-1);
    Pixel<float, N> sample = img(samplePoint[0], samplePoint[1]);

    int xbegin = std::max(0, xbase - filter_size[1]);
    int ybegin = std::max(0, ybase - filter_size[0]);

    int xend = std::min(static_cast<int>(cols), xbase+1 + filter_size[1]);
    int yend = std::min(static_cast<int>(rows), ybase+1 + filter_size[0]);

    float best = 0.0f;
    auto best_p = center;
    for(int y = ybegin; y < yend; ++y) {
        for(int x = xbegin; x < xend; ++x) {
            float pdf_val = probForParamsGivenSample(params(y,x), sample);
            if(best < pdf_val) {
                best = pdf_val;
                best_p = Eigen::Vector2i(y,x);
            }
        }
    }
    assert(best >= 0);
    return best_p;
}

static std::vector<Eigen::Vector2i> neighborhood_around(int rows, int cols, Eigen::Vector2i center, int filter_size) {
    int xbase = center(1);
    int ybase = center(0);

    int xbegin = std::max(0, xbase - filter_size);
    int ybegin = std::max(0, ybase - filter_size);

    int xend = std::min(static_cast<int>(cols), xbase+1 + filter_size);
    int yend = std::min(static_cast<int>(rows), ybase+1 + filter_size);

    std::vector<Eigen::Vector2i> out;
    for(int y = ybegin; y < yend; ++y) {
        for(int x = xbegin; x < xend; ++x) {
            out.push_back({y,x});
        }
    }
    return out;
}

template<typename ProbForParamsGivenSample, typename Parameters, typename Value, int N>
std::pair<std::vector<Eigen::Vector2i>, std::vector<Eigen::Vector2i>> select_neighborhoods_no_overlap(ProbForParamsGivenSample probForParamsGivenSample, const Image<Value, N>& img, const Eigen::Matrix<Parameters, Eigen::Dynamic, Eigen::Dynamic>& parameters, int search_extent, int filter_extent, Eigen::Vector2i p1, Eigen::Vector2i p2) {
    auto search_center1 = p1;
    auto search_center2 = p2;
    Eigen::Vector2i search_extent_vec { search_extent, search_extent };

    if(p1[0] == p2[0]) {
        // horizontal case
        assert(p1[1] > p2[1]);
        search_extent_vec[1] = 0;
        search_center1[1] += search_extent;
        search_center2[1] -= search_extent;
    } else {
        // vertical case
        assert(p1[1] == p2[1]);
        assert(p1[0] > p2[0]);
        search_extent_vec[0] = 0;
        search_center1[0] += search_extent;
        search_center2[0] -= search_extent;
    }

    auto best_center1 = best_neighborhood(probForParamsGivenSample, img, parameters, p1, search_center1, search_extent_vec);
    auto best_center2 = best_neighborhood(probForParamsGivenSample, img, parameters, p2, search_center2, search_extent_vec);

    int rows = img.rows();
    int cols = img.cols();

    auto neighborhood1 = neighborhood_around(rows, cols, best_center1, filter_extent);
    auto neighborhood2 = neighborhood_around(rows, cols, best_center2, filter_extent);

    return {
        neighborhood1,
        neighborhood2
    };
}

template<typename ProbForParamsGivenSample, typename Parameters, int N>
std::pair<std::vector<Eigen::Vector2i>, std::vector<Eigen::Vector2i>> select_neighborhoods(ProbForParamsGivenSample probForParamsGivenSample, const Image<float, N>& img, const Eigen::Matrix<Parameters, Eigen::Dynamic, Eigen::Dynamic>& parameters, int search_extent, int filter_extent, Eigen::Vector2i p1, Eigen::Vector2i p2) {
    Eigen::Vector2i search_extent_vec { search_extent, search_extent };
    auto best_center1 = best_neighborhood(probForParamsGivenSample, img, parameters, p1, p1, search_extent_vec);
    auto best_center2 = best_neighborhood(probForParamsGivenSample, img, parameters, p2, p2, search_extent_vec);

    int rows = img.rows();
    int cols = img.cols();

    auto neighborhood1 = neighborhood_around(rows, cols, best_center1, filter_extent);
    auto neighborhood2 = neighborhood_around(rows, cols, best_center2, filter_extent);

    return {
        neighborhood1,
        neighborhood2
    };
}

template<typename Similarity, typename ProbForParamsGivenSample, typename Parameters, int N>
float dynamic_neighborhood_similarity(Similarity similarity, ProbForParamsGivenSample probForParamsGivenSample, const Image<float, N>& img, const Eigen::Matrix<Parameters, Eigen::Dynamic, Eigen::Dynamic>& parameters, int search_extent, int filter_extent, Eigen::Vector2i p1, Eigen::Vector2i p2) {

    //auto [neighborhood1, neighborhood2] = select_neighborhoods_no_overlap(probForParamsGivenSample, img, parameters, search_extent, filter_extent, p1, p2);
    auto [neighborhood1, neighborhood2] = select_neighborhoods(probForParamsGivenSample, img, parameters, search_extent, filter_extent, p1, p2);

    // Not required due to inherent order of values
    //std::sort(neighborhood1.begin(), neighborhood1.end(), cmp_linear);
    //std::sort(neighborhood2.begin(), neighborhood2.end(), cmp_linear);

    std::vector<Eigen::Vector2i> overlap;
    std::set_intersection (
            neighborhood1.begin(), neighborhood1.end(),
            neighborhood2.begin(), neighborhood2.end(),
            std::back_inserter(overlap), cmp_linear);

    Eigen::Vector2i diff = (p1-p2).transpose();
    std::sort(overlap.begin(), overlap.end(), [&](const auto& o1, const auto& o2) {
            //return (dist_sq(p1, o1)-dist_sq(p2,o1)) < (dist_sq(p1, o2)-dist_sq(p2,o2));
            //return dist_sq(p1, o1) < dist_sq(p1, o2);
            //return dist_sq(p2, o1) > dist_sq(p2, o2);
            int d = diff.dot(o1 - o2);
            if(d==0) {
                return linear_order(o1) < linear_order(o2);
            } else {
                // diff goes from p2 to p1, i.e., it "points towards the p1 side".
                // Consequently, if o1 is farther on the p1 side than o2, d is positive.
                return d > 0;
            }
            });

    auto o1begin = overlap.begin();
    auto o1end = overlap.begin()+overlap.size()/2;
    auto o2begin = o1end;
    auto o2end = overlap.end();

    std::vector<Eigen::Vector2i> o1(o1begin, o1end);
    std::vector<Eigen::Vector2i> o2(o2begin, o2end);
    std::sort(o1.begin(), o1.end(), cmp_linear);
    std::sort(o2.begin(), o2.end(), cmp_linear);

    std::vector<Eigen::Vector2i> n1final;
    std::vector<Eigen::Vector2i> n2final;

    std::set_difference(neighborhood1.begin(), neighborhood1.end(), o2.begin(), o2.end(), std::back_inserter(n1final), cmp_linear);
    std::set_difference(neighborhood2.begin(), neighborhood2.end(), o1.begin(), o1.end(), std::back_inserter(n2final), cmp_linear);

    float w = similarity(img, n1final, n2final);
    return w;
}

template<int N>
ManualParameter<N>::ManualParameter(const Image<float, N>& img_orig, float betap)
    : img(img_orig)
    , beta()
{
    int rows = img.rows();
    int cols = img.cols();
    float max_sqr_diff = 0;
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            Eigen::Vector2i pos(y,x);
            Pixel<float, N> v1 = sample(img, pos);
            for(int d = 0; d < 2; ++d) {
                if(pos[d] > 0) {
                    auto neigh = pos;
                    neigh[d] -= 1;

                    Pixel<float, N> v2 = sample(img, neigh);

                    Pixel<float, N> diff = v1-v2;
                    Pixel<float, 1> diffsq_mat = diff.transpose()*diff;
                    float diffsq = diffsq_mat[0];

                    max_sqr_diff = std::max(max_sqr_diff, diffsq);
                }
            }
        }
    }

    beta = betap / max_sqr_diff;
}

template<int N>
float ManualParameter<N>::weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const {
    auto [v1, v2] = sample(img, p1, p2);
    Pixel<float,N> diff = v1-v2;
    Pixel<float, 1> diffsq_mat = diff.transpose()*diff;
    float diffsq = diffsq_mat[0];

    float w = std::exp(-diffsq*beta);
    //float minweight = 1e-5;
    //return std::max(w, minweight);
    return w;
}


template<int N>
GlobalGaussianParameterGeneric<N>::GlobalGaussianParameterGeneric(const Image<float, N>& orig_img, int search_extent, int filter_extent)
    : img(orig_img)
    , estimatedParams()
    , covariance_inv()
    , search_extent(search_extent)
    , filter_extent(filter_extent)
{
    estimatedParams = meanFilterClamped(img, filter_extent, filter_extent);

    int rows = img.rows();
    int cols = img.cols();
    int fs = size(filter_extent);
    int xbegin = fs;
    int ybegin = fs;
    int xend = cols-fs;
    int yend = rows-fs;

    size_t size = orig_img(0,0).size();
    Matrix cov_sum = Matrix::Zero(size, size);
    for(int y = ybegin; y < yend; ++y) {
        for(int x = xbegin; x < xend; ++x) {
            Pixel<float, N> o = img(y,x);
            Pixel<float, N> m = estimatedParams(y,x);
            Pixel<float, N> diff = o-m;

            cov_sum += diff*diff.transpose();
        }
    }
    cov_sum *= blur_correction_factor(fs, fs);

    assert(xend > xbegin);
    assert(yend > ybegin);
    int num_voxels = (xend-xbegin)*(yend-ybegin);
    Matrix covariance_matrix = cov_sum/num_voxels;
    covariance_inv = covariance_matrix.inverse();
    if(covariance_inv.array().isInf().any()) {
        throw RWException("Estimated inverse covariance matrix is infinite in at least one element.");
    }
    assert(!covariance_inv.array().isNaN().any());
}

template<int N>
float GlobalGaussianParameterGeneric<N>::weight(Eigen::Vector2i p1, Eigen::Vector2i p2) const {
    auto gaussianSimilarity = [&] (const Image<float, N>& img, std::vector<Eigen::Vector2i> neighborhood1, std::vector<Eigen::Vector2i> neighborhood2) {
        if(neighborhood1.size() > neighborhood2.size()) {
            neighborhood1.resize(neighborhood2.size());
        } else if(neighborhood1.size() < neighborhood2.size()) {
            neighborhood2.resize(neighborhood1.size());
        }
        size_t n = neighborhood1.size();
        assert(n == neighborhood2.size());

        auto mean = [&] (const std::vector<Eigen::Vector2i>& vals) -> Pixel<float, N> {

            Pixel<float, N> sum = zero_element(img);
            for(const auto& p : vals) {
                sum += sample(img, p);
            }
            return sum/vals.size();
        };

        Pixel<float, N> mean1 = mean(neighborhood1);
        Pixel<float, N> mean2 = mean(neighborhood2);

        Pixel<float, N> diff = mean1-mean2;

        Pixel<float, 1> coeff = diff.transpose() * covariance_inv * diff / 8.0f * n;

        float w = std::exp(-coeff[0]);

        assert(!std::isnan(w) && std::isfinite(w) && w >= 0);

        return w;
    };

    auto probForParamsGivenSample = [&] (Pixel<float, N> mu, Pixel<float, N> sample) -> float {

        Pixel<float, N> diff = mu-sample;

        Pixel<float, 1> coeff = diff.transpose() * covariance_inv * diff / 2.0f;

        float w = std::exp(-coeff[0]);

        return w;
    };

    return dynamic_neighborhood_similarity(gaussianSimilarity, probForParamsGivenSample, img, estimatedParams, search_extent, filter_extent, p1, p2);
}
