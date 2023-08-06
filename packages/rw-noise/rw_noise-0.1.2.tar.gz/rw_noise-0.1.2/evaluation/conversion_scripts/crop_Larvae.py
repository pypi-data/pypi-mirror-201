from PIL import Image
import numpy as np
import os

path = '/data/home/f_eile01/sciebo/Random_Walker_data/Larvae_Imida_WT_rnd'

for files in os.listdir(path):
    if '.py' in files or 'crop' in files:
        continue
    im = Image.open(os.path.join(path, files))
    na = np.array(im)[750:1250, 750:1250]
    data = Image.fromarray(na)

    data.save(os.path.join(path, 'cropped', files))
