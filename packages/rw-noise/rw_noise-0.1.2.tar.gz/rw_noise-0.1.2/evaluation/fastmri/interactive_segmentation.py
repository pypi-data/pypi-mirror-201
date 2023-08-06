#!/usr/bin/env python3
import h5py
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util
import numpy as np
import data


files = data.data_files()

def id(img):
    return img

def magnitude(img):
    return np.linalg.norm(img, axis=2)

methods = [
        util.fixed(500),
        util.fixed(500),
        util.global_gaussian(2),
        util.global_gaussian(2),
        util.ttest(2),
        util.variable_gaussian(2),
        util.global_gaussian_bian(2),
        ]

converters = [
        id,
        magnitude,
        id,
        magnitude,
        magnitude,
        magnitude,
        magnitude,
        ]

for i in range(len(files)):
    img, _, _ = data.load_file(files, i)
    util.run_interactive_label_loop(img, methods, converters)
