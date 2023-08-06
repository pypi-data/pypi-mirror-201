#pragma once

#include <string>
#include <Eigen/Eigen>

class RWException : public std::exception {
public:
    RWException(std::string msg)
        : msg(msg)
    {
    }
    ~RWException() {
    }
    const char *what() const throw() {
        return msg.c_str();
    }
private:
    std::string msg;
};


template<typename T, int size>
using Pixel = Eigen::Matrix<T, size, 1>;

template<typename T, int size>
using Image = Eigen::Matrix<Pixel<T, size>, Eigen::Dynamic, Eigen::Dynamic>;

Image<float, 1> round(Image<float, 1> img);

Image<float, 1> medianFilter(const Image<float, 1>& img, int H_Extent, int W_Extent);

constexpr int size(int extent) {
    return 2*extent+1;
}
constexpr int filter_size(int h, int w) {
    return size(w)*size(h);
}
constexpr float blur_correction_factor(int h, int w) {
    int f_size = filter_size(h,w);
    return static_cast<float>(f_size)/(f_size-1);
}

template<int N>
Pixel<float, N> zero_element(const Image<float, N>& img) {
    size_t size = img(0,0).size();
    return Pixel<float, N>::Zero(size);
}

Image<float, 1> variances(const Image<float, 1>& img, const Image<float, 1>& means, int hExtent, int wExtent);

template<typename T, int N>
Image<T, N> sumFilter(const Image<T, N>& img, int height, int width) {
    int rows = img.rows() - height + 1;
    int cols = img.cols() - width + 1;

    Image<T, N> tmp(img.rows(), cols);
    for(int y = 0; y < img.rows(); ++y) {
        for(int x = 0; x < cols; ++x) {
            Pixel<T, N> sum = zero_element(img);
            for(int dx = 0; dx < width; ++dx) {
                sum += img(y,x+dx);
            }
            tmp(y,x) = sum;
        }
    }

    Image<T, N> res(rows, cols);
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            Pixel<T, N> sum = zero_element(img);
            for(int dy = 0; dy < height; ++dy) {
                sum += tmp(y+dy,x);
            }
            res(y,x) = sum;
        }
    }

    return res;
}

template<typename T, int N>
Image<T, N> meanFilterClamped(const Image<T, N>& img, int hExtent, int wExtent) {
    int rows = img.rows();
    int cols = img.cols();

    Image<T, N> tmp(rows,cols);
    float num_w_inv = 1.0/size(wExtent);
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            Pixel<T, N> sum = zero_element(img);
            assert(!sum.array().isNaN().any() && !sum.array().isInf().any());
            for(int dx = -wExtent; dx <= wExtent; ++dx) {
                sum += img(y,std::clamp(x+dx, 0, cols-1));
                assert(!sum.array().isNaN().any() && !sum.array().isInf().any());
            }
            tmp(y,x) = sum*num_w_inv;
        }
    }

    Image<T, N> mean(rows, cols);
    float num_h_inv = 1.0/size(hExtent);
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            Pixel<T, N> sum = zero_element(img);
            assert(!sum.array().isNaN().any() && !sum.array().isInf().any());
            for(int dy = -hExtent; dy <= hExtent; ++dy) {
                sum += tmp(std::clamp(y+dy, 0, rows-1),x);
                assert(!sum.array().isNaN().any() && !sum.array().isInf().any());
            }
            mean(y,x) = sum*num_h_inv;
        }
    }

    return mean;
}

template<typename T, int N>
Image<float, 1> magnitude(const Image<T, N>& img) {
    int rows = img.rows();
    int cols = img.cols();

    Image<float, 1> result(rows,cols);
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            const auto& p = img(y,x);
            Pixel<float, 1> mag2 = p.transpose() * p;
            Pixel<float, 1> magnitude{ std::sqrt(mag2[0])};
            result(y,x) = magnitude;
        }
    }

    return result;
}

template<typename T, int N>
static std::pair<Pixel<T, N>, Pixel<T, N>> sample(const Image<T, N>& img, Eigen::Vector2i p1, Eigen::Vector2i p2) {
    return std::make_pair(
            img(p1(0), p1(1)),
            img(p2(0), p2(1))
            );
}

template<typename T, int N>
Pixel<T, N> sample(const Image<T, N>& img, Eigen::Vector2i p1) {
    return img(p1(0), p1(1));
}
