#!/usr/bin/env python3
import sys
import numpy as np
import re
from os import path, listdir
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util

data_dir = path.expanduser("~/sciebo/Random_Walker_data/Larvae_Imida_WT_rnd/cropped")
region_pattern = "(.*)_mask.npy"

def data_files():
    data = []
    for f in listdir(data_dir):
        m = re.match(region_pattern, f)
        if m:
            prefix = m[1]
            mask_file = path.join(data_dir, f)
            img_file = path.join(data_dir, prefix + ".npy")
            data.append((img_file, mask_file))
    data = sorted(data)
    return data


def load_file(files, i):
    imgfile, maskfile = files[i]

    img = np.load(imgfile).astype(np.float32)
    mask = np.load(maskfile).astype(int)
    num_classes = np.max(mask)
    alpha, beta = util.estimate_scaled_poisson_parameters(img)
    img = (img-beta)/alpha
    img = np.maximum(0, img)
    num_classes = np.max(mask)

    return img, mask, num_classes
