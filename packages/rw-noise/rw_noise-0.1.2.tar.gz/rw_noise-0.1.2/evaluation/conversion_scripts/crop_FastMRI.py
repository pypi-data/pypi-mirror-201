from PIL import Image
import numpy as np
import os

path = '/data/home/f_eile01/sciebo/Random_Walker_data/FastMRI_reconstructed/'

for masks in os.listdir(path):
    if not '_mask.png' in masks:
        continue
    print(masks)
    mask_pil = Image.open(os.path.join(path, masks))
    mask_na = np.array(mask_pil)[120:520, :]
    mask_data = Image.fromarray(mask_na)
    mask_data.save(os.path.join(path, 'cropped', masks))

    masks_split = masks.split('_')
    image = masks_split[0] + '_' + masks_split[1] + '.png'
    print(image)

    image_pil = Image.open(os.path.join(path, image))
    image_na = np.array(image_pil)[120:520, :]
    image_data = Image.fromarray(image_na)
    image_data.save(os.path.join(path, 'cropped', image))

    
