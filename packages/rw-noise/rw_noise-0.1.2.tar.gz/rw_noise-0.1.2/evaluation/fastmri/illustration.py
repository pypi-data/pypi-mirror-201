#!/usr/bin/env python3
import argparse
import sys
import numpy as np
from PIL import Image
from matplotlib import cm
import re
import data
from os import path, listdir
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util

parser = argparse.ArgumentParser()
parser.add_argument("output", type=str, help="Write figures to specified folder")
args = parser.parse_args()

files = data.data_files()
index_to_show = [i for i, (_, f, _) in enumerate(files) if "file1000052" in f][0]
print(index_to_show)
overlay_alpha = 50
num_improvements = 10


print(files[index_to_show])
img, mask, num_classes = data.load_file(files, index_to_show)
mag = np.linalg.norm(img, axis=2)

seeds = util.generate_initial_seeds(mask, num_classes)

def save(array, name):
    im = Image.fromarray(array)
    im.save(path.join(args.output, "mri_illustration_" + name + ".png"))

def class_img(classes, alpha):
    return util.labels_to_img_array(classes, alpha)


def probimg(img, method, alpha):
    classes, seeds = util.run_rw_simulation_prediction_after(img.astype(np.float32), method, mask, num_classes, num_improvements)
    voi = util.voi(mask, classes, num_classes)
    arand = util.arand(mask, classes)
    print(f"{method['name']}: voi: {voi}")
    print(f"{method['name']}: arand: {arand}")
    prediction_img = class_img(classes, alpha)
    seed_img = class_img(seeds, 255)
    return prediction_img, seed_img

def composite_seeds(img):
    img = util.gray(img, 255)
    seed_img = class_img(seeds, 255)
    return util.composite(img, seed_img)

def show_method(run_img, method, name):
    prediction_img, seed_img = probimg(run_img, method, overlay_alpha)

    to_show = util.gray(mag, 255)
    to_show = util.composite(to_show, prediction_img)
    to_show = util.composite(to_show, seed_img)
    #to_show = np.swapaxes(to_show, 0, 1)
    save(to_show, name)

save(composite_seeds(mag), "img_with_seeds")
save(util.composite(util.gray(mag, 255), class_img(mask, overlay_alpha)), "ground_truth")

show_method(mag, util.global_gaussian_bian(2), "global_gaussian_bian")
show_method(mag, util.fixed(10000), "grady_mag")
show_method(img, util.fixed(3981.0717055349774), "grady_2d")
show_method(mag, util.global_gaussian(2), "global_gaussian_mag")
show_method(img, util.global_gaussian(2), "global_gaussian_2d")
