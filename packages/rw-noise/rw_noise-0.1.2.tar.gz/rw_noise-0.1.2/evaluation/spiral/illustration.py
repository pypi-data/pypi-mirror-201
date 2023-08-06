#!/usr/bin/env python3
import argparse
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util
import numpy as np
import math
import data
from PIL import Image
from matplotlib import cm

parser = argparse.ArgumentParser()
parser.add_argument("output", type=str, help="Write figures to specified folder")
args = parser.parse_args()

flatColor = True
seed = 4


def save(array, name):
    im = Image.fromarray(array)
    im.save(path.join(args.output, "spiral_" + name + ".png"))

def class_img(classes):
    out = np.zeros((classes.shape[0], classes.shape[1], 3), dtype=np.uint8)
    out[classes == 2, 0] = 255
    out[classes == 1, 2] = 255
    return out


def probimg(img, method):
    classes, probs = util.run_rw(img.astype(np.float32), seeds, method)
    if flatColor:
        return class_img(classes)
    else:
        return np.uint8(cm.bwr(probs[0])*255)[:,:,0:3]


def composite(img, pimg):
    base = util.gray(img)
    return (base /2 + pimg /2).astype(np.uint8)

def composite_seeds(img):
    out = util.gray(img)
    seed_img = class_img(seeds)
    out[seeds != 0] = seed_img[seeds != 0]
    return out

gt_scalar = data.gen_image(lambda _: 0, lambda p: 1)
gt_vector = data.gen_image(lambda p: data.tangent(p), lambda p: -data.tangent(p), np.complex64)
gt_phase = np.angle(gt_vector)
seeds = data.seed_image()

save(composite_seeds(gt_scalar), "gt_scalar")
save(composite_seeds(gt_phase), "gt_vector")


np.random.seed(seed)
poisson_noisy = np.random.poisson(data.gen_image(lambda _: 32, lambda _: 64))

save(composite(poisson_noisy, probimg(poisson_noisy, util.poisson(2))), "poisson_ours")
save(composite(poisson_noisy, probimg(poisson_noisy, util.ttest(2))), "poisson_ttest")
save(composite(poisson_noisy, probimg(poisson_noisy, util.fixed(398))), "poisson_grady")

np.random.seed(seed)
loupas_noisy = data.apply_loupas_noise(data.gen_image(lambda _: 0.1, lambda _: 1), 0.2)

save(composite(loupas_noisy, probimg(loupas_noisy, util.variable_gaussian(2))), "loupas_ours")
save(composite(loupas_noisy, probimg(loupas_noisy, util.ttest(2))), "loupas_ttest")
save(composite(loupas_noisy, probimg(loupas_noisy, util.fixed(100))), "loupas_grady")

np.random.seed(seed)
gaussian_noisy = data.apply_2d_gaussian_noise(util.complex_to_2d(gt_vector), 0.3)
gaussian_noisy_phase = np.angle(util.conv_2d_to_complex(gaussian_noisy))

save(composite(gaussian_noisy_phase, probimg(gaussian_noisy, util.global_gaussian(2))), "gaussian2d_ours")
save(composite(gaussian_noisy_phase, probimg(gaussian_noisy, util.fixed(100))), "gaussian2d_grady")
