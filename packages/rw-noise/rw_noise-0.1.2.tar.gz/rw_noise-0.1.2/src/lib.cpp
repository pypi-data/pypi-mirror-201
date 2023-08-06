#include "boost/python/numpy.hpp"
#include "string.h"
#include "memory.h"
#include <sstream>
#include "imgs.h"
#include "weights.h"
#include "rw.h"

#ifdef USE_MAGMA
#include "magma_v2.h"
#endif

namespace bp = boost::python;
namespace bn = boost::python::numpy;

template<typename T>
Image<T, 1> to_img_scalar(const bn::ndarray& input) {
    if(input.get_nd() != 2) {
        throw RWException("Input array must be two-dimensional");
    }
    if(input.get_dtype() != bn::dtype::get_builtin<T>()) {
        std::stringstream s;
        s << "Input must be of type '";
        s << bp::extract<const char*>(bp::str(bn::dtype::get_builtin<T>()));
        s << "', but is '";
        s << bp::extract<const char*>(bp::str(input.get_dtype()));
        s << "'";
        throw RWException(s.str());
    }

    const auto in_ptr = input.get_data();

    int dimy = input.shape(0);
    int dimx = input.shape(1);
    int stridey = input.strides(0);
    int stridex = input.strides(1);
    Image<T, 1> output(dimy, dimx);
    for(int y = 0; y<dimy; ++y) {
        for(int x = 0; x<dimx; ++x) {
            auto p = reinterpret_cast<const T*>(in_ptr + y*stridey + x*stridex);
            output(y, x) = Pixel<T, 1>(*p);
        }
    }
    return output;
}

template<typename T, int N>
Image<T, N> to_img_nd(const bn::ndarray& input) {
    if(input.get_nd() != 3) {
        throw RWException("Input array must be three-dimensional");
    }

    if(input.get_dtype() != bn::dtype::get_builtin<T>()) {
        std::stringstream s;
        s << "Input must be of type '";
        s << bp::extract<const char*>(bp::str(bn::dtype::get_builtin<T>()));
        s << "', but is '";
        s << bp::extract<const char*>(bp::str(input.get_dtype()));
        s << "'";
        throw RWException(s.str());
    }
    int channels = input.shape(2);
    assert(N == Eigen::Dynamic || channels == N);

    const auto in_ptr = input.get_data();

    int dimy = input.shape(0);
    int dimx = input.shape(1);
    int stridey = input.strides(0);
    int stridex = input.strides(1);
    int stridec = input.strides(2);
    Image<T, N> output(dimy, dimx);
    for(int y = 0; y<dimy; ++y) {
        for(int x = 0; x<dimx; ++x) {
            Pixel<T, N> pixel(channels);
            for(int c = 0; c<channels; ++c) {
                auto p = reinterpret_cast<const T*>(in_ptr + y*stridey + x*stridex + c*stridec);
                pixel(c) = *p;
            }
            output(y, x) = pixel;
        }
    }
    return output;
}

template<typename T>
void write_to_ptr(const Image<T,1>& input, T*& out_ptr) {
    int dimy = input.rows();
    int dimx = input.cols();

    for(int y = 0; y<dimy; ++y) {
        for(int x = 0; x<dimx; ++x) {
            *out_ptr = input(y, x)[0];
            ++out_ptr;
        }
    }
}

template<typename T>
bn::ndarray from_img(const Image<T,1>& input) {
    auto dt = bn::dtype::get_builtin<T>();

    int dimy = input.rows();
    int dimx = input.cols();

    auto out = bn::empty(bp::make_tuple(dimy, dimx), dt);
    auto out_ptr = reinterpret_cast<T*>(out.get_data());

    write_to_ptr(input, out_ptr);
    return out;
}

template<typename T>
bn::ndarray from_imgs(const std::vector<Image<T,1>>& input) {
    assert(!input.empty());
    size_t num_imgs = input.size();
    auto dt = bn::dtype::get_builtin<T>();

    int dimy = input.front().rows();
    int dimx = input.front().cols();

    auto out = bn::empty(bp::make_tuple(num_imgs, dimy, dimx), dt);
    auto out_ptr = reinterpret_cast<T*>(out.get_data());

    for(auto& img : input) {
        assert(img.rows() == dimy);
        assert(img.cols() == dimx);
        write_to_ptr(img, out_ptr);
    }
    return out;
}

std::unique_ptr<Parameters> method_from_dict(const Image<float, 1>& img, const bp::dict& method) {
    std::string name = bp::extract<std::string>(method.get("name"));
    if(name == "fixed") {
        float beta = bp::extract<float>(method.get("beta"));
        return std::make_unique<ManualParameter<1>>(img, beta);
    } else if(name == "global_gaussian_bian") {
        float filter_extent = bp::extract<float>(method.get("filter_extent"));
        return std::make_unique<GlobalGaussianParameterBian>(img, filter_extent);
    } else {
        float search_extent = bp::extract<float>(method.get("search_extent"));
        float filter_extent = bp::extract<float>(method.get("filter_extent"));
        if(name == "ttest") {
            return std::make_unique<TTestParameter>(img, search_extent, filter_extent);
        } else if(name == "global_gaussian") {
            return std::make_unique<GlobalGaussianParameterGeneric<1>>(img, search_extent, filter_extent);
        } else if(name == "variable_gaussian") {
            return std::make_unique<VariableGaussianParameter>(img, search_extent, filter_extent);
        } else if(name == "poisson") {
            return std::make_unique<PoissonParameter>(img, search_extent, filter_extent);
        } else if(name == "loupas") {
            return std::make_unique<LoupasParameter>(img, search_extent, filter_extent);
        }
    }
    std::stringstream s;
    s << "Unknown method name '";
    s << name;
    s << "'";
    throw RWException(s.str());
}

template<int N>
std::unique_ptr<Parameters> method_from_dict_nd(const Image<float, N>& img, const bp::dict& method) {
    std::string name = bp::extract<std::string>(method.get("name"));
    if(name == "fixed") {
        float beta = bp::extract<float>(method.get("beta"));
        return std::make_unique<ManualParameter<N>>(img, beta);
    } else if (name == "global_gaussian") {
        float search_extent = bp::extract<float>(method.get("search_extent"));
        float filter_extent = bp::extract<float>(method.get("filter_extent"));
        return std::make_unique<GlobalGaussianParameterGeneric<N>>(img, search_extent, filter_extent);
    } else if(name == "global_gaussian_bian" || name == "ttest" || name == "variable_gaussian" || name == "poisson") {
        std::stringstream s;
        s << "Method '";
        s << name;
        s << "' only supports scalar input.";
        throw RWException(s.str());
    }

    std::stringstream s;
    s << "Unknown method name '";
    s << name;
    s << "'";
    throw RWException(s.str());
}

bp::tuple weights_from_param(Parameters& param, int rows, int cols) {
    Image<float, 1> weights_horizontal(rows, cols-1);
    Image<float, 1> weights_vertical(rows-1, cols);
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            Eigen::Vector2i pos(y,x);
            Eigen::Vector2i neigh_h(y,x-1);
            Eigen::Vector2i neigh_v(y-1,x);
            if(neigh_h(1) >= 0) {
                weights_horizontal(neigh_h(0), neigh_h(1)) = Pixel<float, 1>(param.weight(pos, neigh_h));
            }
            if(neigh_v(0) >= 0) {
                weights_vertical(neigh_v(0), neigh_v(1)) = Pixel<float, 1>(param.weight(pos, neigh_v));
            }
        }
    }
    return bp::make_tuple(from_img(weights_horizontal), from_img(weights_vertical));
}

bp::tuple rw_weights(const bn::ndarray& in_image, const bp::dict& method) {
    std::unique_ptr<Parameters> param;
    if(in_image.get_nd() < 2 || in_image.get_nd() > 3) {
        throw RWException("Input image must be two- or three-dimensional.");
    }
    int rows = in_image.get_shape()[0];
    int cols = in_image.get_shape()[1];
    if(in_image.get_nd() == 2) {
        auto image = to_img_scalar<float>(in_image);
        param = method_from_dict(image, method);
        return weights_from_param(*param, rows, cols);
    } else {
        int channels = in_image.shape(2);
        switch(channels) {
            case 2: {
                auto image = to_img_nd<float, 2>(in_image);
                param = method_from_dict_nd(image, method);
                return weights_from_param(*param, rows, cols);
            }
            case 3: {
                auto image = to_img_nd<float, 3>(in_image);
                param = method_from_dict_nd(image, method);
                return weights_from_param(*param, rows, cols);
            }
            default: {
                auto image = to_img_nd<float, Eigen::Dynamic>(in_image);
                param = method_from_dict_nd(image, method);
                return weights_from_param(*param, rows, cols);
            }
        }
    }
}

bp::tuple run_rw_wrapper(const bn::ndarray& weights_horizontal, const bn::ndarray& weights_vertical, const bn::ndarray& in_labels) {
    if(in_labels.get_nd() != 2) {
        throw RWException("Label array must be two-dimensional.");
    }
    if(weights_horizontal.get_nd() != 2) {
        throw RWException("Horizontal weight array must be two-dimensional.");
    }
    if(weights_vertical.get_nd() != 2) {
        throw RWException("Vertical weight array must be two-dimensional.");
    }

    auto labels = to_img_scalar<uint32_t>(in_labels);
    size_t num_labels = labels.unaryExpr([] (auto i) { return i[0];}).maxCoeff();
    if(num_labels == 0) {
        throw RWException("No labels specified. All pixel labels are 0.");
    }

    int rows = labels.rows();
    int cols = labels.cols();

    if(weights_horizontal.get_shape()[0] != rows || weights_horizontal.get_shape()[1] != cols-1) {
        throw RWException("Horizontal weight array must have shape (r, c-1) for (r, c) as the shape of labels.");
    }

    if(weights_vertical.get_shape()[0] != rows-1 || weights_vertical.get_shape()[1] != cols) {
        throw RWException("Vertical weight array must have shape (r-1, c) for (r, c) as the shape of labels.");
    }
    auto w_h = to_img_scalar<float>(weights_horizontal);
    auto w_v = to_img_scalar<float>(weights_vertical);

    auto [classes, probabilities] = run_rw(w_h, w_v, labels, num_labels);
    return bp::make_tuple(from_img(classes), from_imgs(probabilities));
}

BOOST_PYTHON_MODULE(rw_noise) {
#ifdef USE_MAGMA
    magma_init();
#endif
    bn::initialize();
    bp::def("solve", run_rw_wrapper);
    bp::def("weights", rw_weights);
}
