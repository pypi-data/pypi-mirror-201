#!/usr/bin/env python3
import h5py
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util
import numpy as np


def gen_image(size, bgval):
    image = np.tile(bgval, (size[0], size[1], 1))

    centers = [(y*size[0], x*size[1]) for y, x in [(0.25,0.25), (0.75, 0.25), (0.25,0.75), (0.75, 0.75)]]
    radii = [size[0]/8 for _ in centers]
    values = [(1,0), (0, -1), (1, 1), (0, 0)]

    yy, xx = np.mgrid[:size[0], :size[1]]
    for center, radius, value in zip(centers, radii, values):
        circle = (xx - center[0]) ** 2 + (yy - center[1]) ** 2
        inside = circle < radius*radius
        image[inside] = value

    image = image.astype(np.float32)
    noise = np.random.multivariate_normal((0, 0), [[0.1, 0.0], [0.0, 0.1]], size)
    image += noise

    return image



size = (256, 256)

methods = [
        util.fixed(5),
        util.fixed(50),
        util.fixed(500),
        util.global_gaussian(2),
        ]

bgval = np.array([0,1])
while True:
    img = gen_image(size, bgval)
    #util.show_image(img)
    #img[0] = np.random.normal(img[0], 1)
    #img[1] = np.random.normal(img[1], 1)
    util.run_interactive_label_loop(img, methods)
