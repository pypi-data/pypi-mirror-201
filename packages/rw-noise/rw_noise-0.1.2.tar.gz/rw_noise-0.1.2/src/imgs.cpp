#include "imgs.h"
#include <iostream>
#include <unordered_map>

Image<float, 1> round(Image<float, 1> img) {
    int rows = img.rows();
    int cols = img.cols();

    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            img(y,x) = Pixel<float,1>{std::round(img(y,x)[0])};
        }
    }
    return img;
}

Image<float, 1> medianFilter(const Image<float, 1>& img, int hExtent, int wExtent) {
    int rows = img.rows();
    int cols = img.cols();

    Image<float, 1> medians(rows, cols);
    std::vector<float> vals(filter_size(wExtent,hExtent), 0.0f) ;
    for(int ybase = 0; ybase < rows; ++ybase) {
        for(int xbase = 0; xbase < cols; ++xbase) {
            int i = 0;

            int xbegin = std::max(0, xbase - wExtent);
            int ybegin = std::max(0, ybase - hExtent);

            int xend = std::min(static_cast<int>(cols), xbase+1 + wExtent);
            int yend = std::min(static_cast<int>(rows), ybase+1 + hExtent);

            for(int y = ybegin; y < yend; ++y) {
                for(int x = xbegin; x < xend; ++x) {
                    vals[i] = img(y,x)[0];
                    i+=1;
                }
            }
            auto end = vals.begin()+i;
            const auto median_it = vals.begin() + i / 2;
            std::nth_element(vals.begin(), median_it , end);
            float median = *median_it;

            medians(ybase,xbase) = Pixel<float, 1>(median);
        }
    }

    return medians;
}

Image<float, 1> variances(const Image<float, 1>& img, const Image<float, 1>& means, int hExtent, int wExtent) {
    int rows = img.rows();
    int cols = img.cols();

    Image<float, 1> var(rows,cols);
    for(int ybase = 0; ybase < rows; ++ybase) {
        for(int xbase = 0; xbase < cols; ++xbase) {

            int xbegin = std::max(0, xbase - wExtent);
            int ybegin = std::max(0, ybase - hExtent);

            int xend = std::min(static_cast<int>(cols), xbase+1 + wExtent);
            int yend = std::min(static_cast<int>(rows), ybase+1 + hExtent);

            float sum = 0.0f;
            float mean = means(ybase,xbase)[0];
            for(int y = ybegin; y < yend; ++y) {
                for(int x = xbegin; x < xend; ++x) {
                    float diff = mean - img(y,x)[0];
                    sum += diff*diff;
                }
            }
            float num = (xend-xbegin)*(yend-ybegin);
            var(ybase,xbase) = Pixel<float, 1>{sum/(num-1)};
        }
    }

    return var;
}
