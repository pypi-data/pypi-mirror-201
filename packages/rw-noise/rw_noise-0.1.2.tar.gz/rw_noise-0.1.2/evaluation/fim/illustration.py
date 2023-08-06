#!/usr/bin/env python3
import argparse
import sys
import numpy as np
from PIL import Image
import data
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util

parser = argparse.ArgumentParser()
parser.add_argument("output", type=str, help="Write figures to specified folder")
args = parser.parse_args()

index_to_show = 3
overlay_alpha = 100

data_dir = path.expanduser("~/sciebo/Random_Walker_data/Larvae_Imida_WT_rnd/cropped")
region_pattern = "(.*)_mask.npy"

files = data.data_files()

img, mask, num_classes = data.load_file(files, index_to_show)

seeds = util.generate_initial_seeds(mask, num_classes)

def save(array, name):
    im = Image.fromarray(array)
    im.save(path.join(args.output, "fim_illustration_" + name + ".png"))

def class_img(classes, alpha):
    return util.labels_to_img_array(classes, alpha)


def probimg(img, method, alpha):
    classes, probs = util.run_rw(img.astype(np.float32), seeds, method)
    voi = util.voi(mask, classes, num_classes)
    arand = util.arand(mask, classes)
    print(f"{method['name']}: voi: {voi}")
    print(f"{method['name']}: arand: {arand}")
    return class_img(classes, alpha)

def composite_seeds(img):
    img = util.gray(img, 255)
    seed_img = class_img(seeds, 255)
    return util.composite(img, seed_img)

def show_method(method, name):
    save(util.composite(util.gray(img, 255), probimg(img, method, overlay_alpha)), name)

save(composite_seeds(img), "img_with_seeds")
save(util.composite(util.gray(img, 255), class_img(mask, overlay_alpha)), "ground_truth")

show_method(util.variable_gaussian(2), "variable_gaussian")
show_method(util.poisson(2), "poisson")
show_method(util.ttest(2), "ttest")
show_method(util.fixed(158.48931924611142), "grady")
