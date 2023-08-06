#!/usr/bin/env python3
import sys
import numpy as np
import re
from os import path, listdir
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util

data_dir = path.expanduser("~/sciebo/Random_Walker_data/FastMRI_reconstructed/")
region_pattern = "(.*)_(\d+)_mask.npy"

def data_files():
    data = []
    for f in listdir(data_dir):
        m = re.match(region_pattern, f)
        if m:
            prefix = m[1]
            z = int(m[2])
            mask_file = path.join(data_dir, f)
            img_file = path.join(data_dir, prefix + ".npy")
            data.append((z,img_file,mask_file))

    data = sorted(data)
    return data

y_begin = 150
y_end = 500
#y_begin = 100
#y_end = 540
#y_begin = 180
#y_end = 420

# It is recommended to multiply the images to be around 1 to avoid machine precision issues.
const_multiplier = 1e6


expected_num_classes_complex = 7
#Original classes (complex) are:
# 1: Upper bone
# 2: cartilage
# 3: left meniscus
# 4: other leg tissue
# 5: right meniscus
# 6: lower bone
# 7: background

#Original classes (complex) are:
# 1: Upper bone
# 4: other leg tissue
# 6: lower bone
# 7: background

expected_num_classes = 4
#simplified classes are:
# 1: Upper bone
# 2: Lower bone
# 3: Other leg tissue
# 4: Background


def remap_classes(img):
    class_map_complex = [
        0, #unused
        1, #upper bone => upper bone
        3, #cartilage => other leg tissue
        3, #left meniscus => other leg tissue
        3, #other leg tissue => other leg tissue
        3, #right meniscus => other leg tissue
        2, #lower bone => lower bone
        4, #background => background
    ]
    class_map_simple = [
        0, #unused
        1, #upper bone => upper bone
        3, #other leg tissue => other leg tissue
        2, #lower bone => lower bone
        4, #background => background
    ]
    def apply_class_map_complex(v):
        return class_map_complex[v]
    def apply_class_map_simple(v):
        return class_map_simple[v]

    num_classes_orig = np.max(img)
    if num_classes_orig == len(class_map_complex) - 1:
        return np.vectorize(apply_class_map_complex)(img)
    elif num_classes_orig == len(class_map_simple) - 1:
        return np.vectorize(apply_class_map_simple)(img)
    else:
        assert(False, "invalid number of classes in original image")

def load_file(files, i):
    z, imgfile, maskfile = files[i]

    img_full = np.load(imgfile)
    img = util.complex_to_2d(img_full[z,:,:])
    img *= const_multiplier
    mask = np.load(maskfile).astype(int)

    img = img[y_begin:y_end, :, :]
    mask = mask[y_begin:y_end, :]

    num_classes_orig = np.max(mask)
    mask = remap_classes(mask)

    num_classes = np.max(mask)
    if num_classes != expected_num_classes:
        print(f"Not exactly {expected_num_classes} classes in file {maskfile} ({num_classes})")
        util.show_image(mask)
        print(mask)
        assert(False)

    return img, mask, num_classes
