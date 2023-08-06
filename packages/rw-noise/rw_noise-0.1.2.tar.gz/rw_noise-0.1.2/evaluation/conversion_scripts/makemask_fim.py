#!/usr/bin/env python3
import numpy as np
import imageio
import os
import matplotlib.pyplot as plt
import re

data_dir = os.path.expanduser('~/sciebo/Random_Walker_data/Larvae_Imida_WT_rnd/cropped')

def find_values(im):
    shape = im.shape
    all_vals = []
    for i in range(shape[0]):
        for j in range(shape[1]):
            if not True in (np.all(im[i, j, :] == ar) for ar in all_vals):
                all_vals.append(im[i, j, :])
    return all_vals

mask_pattern = "(.*_mask).tiff"
file_pattern = "(.*).tiff"

for f in os.listdir(data_dir):
    m = re.match(file_pattern, f)
    if m:
        file = os.path.join(data_dir, f);
        if re.match(mask_pattern, f):
            mask = imageio.imread(file)
            mask = mask[:, :, :3] # 4 is alpha if its there
            out_prefix = m[1]
            out_file = os.path.join(data_dir, out_prefix + ".npy");
            if os.path.exists(out_file):
                print(f"Skipping existing file {out_file}")
                continue

            print(f"Converting file {out_file}")

            all_vals = find_values(mask)
            all_vals = sorted(all_vals, key=lambda k: (k[0], k[1], k[2]))

            if len(all_vals) < 2:
                print(f"Only one color in mask!")
                print(all_vals)
                assert(False)

            masks = np.zeros([mask.shape[0], mask.shape[1]], dtype=np.uint32)

            for i in range(len(all_vals)):
                masks = np.maximum(masks, (i+1)*np.all(mask == all_vals[i], axis = 2))
            assert(np.min(masks) == 1)
            #plt.imshow(masks[:, :], cmap='gray')
            #plt.show()
            np.save(out_file, masks)
        else:
            out_prefix = m[1]
            out_file = os.path.join(data_dir, out_prefix + ".npy");
            if os.path.exists(out_file):
                print(f"Skipping existing file {out_file}")
                continue
            img = imageio.imread(file)
            print(f"Converting file {out_file}")
            np.save(out_file, img)
