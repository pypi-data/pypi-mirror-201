#pragma once

#include "imgs.h"
#include "weights.h"

std::pair<Image<uint32_t, 1>,std::vector<Image<float, 1>>> run_rw(const Image<float, 1> weights_horizontal, const Image<float, 1> weights_vertical, const Image<uint32_t, 1>& labels, size_t num_classes);
