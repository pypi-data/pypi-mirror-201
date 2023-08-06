import numpy as np
import math

size = (200, 200)

circle_radius = math.pi * 6


def pixel_to_complex(y, x):
    p_r = 2*x/size[1] - 1
    p_i = 2*y/size[0] - 1
    p = p_r + 1j*p_i
    p *= circle_radius
    return p


def complex_to_pixel(c):
    c /= circle_radius
    p_r = np.real(c)
    p_i = np.imag(c)

    x = (p_r - 1)/2 * size[1]
    y = (p_i - 1)/2 * size[0]

    return round(y), round(x)


def gen_image(fgval_fun, bgval_fun, dtype=np.float32):
    image = np.zeros(size, dtype=dtype)

    for y in range(size[0]):
        for x in range(size[1]):
            p = pixel_to_complex(y, x)

            if np.absolute(p) > circle_radius:
                p = p/np.absolute(p)*circle_radius

            phase = np.angle(p) - np.absolute(p)
            phase += math.ceil(math.fabs(phase)) * 2 * math.pi
            phase = math.fmod(phase, 2 * math.pi)

            if phase > math.pi:
                val = bgval_fun(p)
            else:
                val = fgval_fun(p)

            image[y, x] = val

    return image


def seed_image():
    image = np.zeros(size, dtype=np.uint32)

    y_bg, x_bg = complex_to_pixel(math.pi*0.5)
    y_fg, x_fg = complex_to_pixel(-math.pi*0.5)

    image[y_bg, x_bg] = 1
    image[y_fg, x_fg] = 2

    return image


def tangent(p):
    if p == 0:
        return 0

    norm = p/np.absolute(p)
    return norm * 1j


def apply_loupas_noise(img, sigma):
    noise = np.random.normal(np.zeros(img.shape), sigma)
    img = img + np.sqrt(img) * noise
    return img.astype(np.float32)


def apply_2d_gaussian_noise(img, sigma):
    img[:,:,0] = np.random.normal(img[:,:,0], sigma)
    img[:,:,1] = np.random.normal(img[:,:,1], sigma)
    return img.astype(np.float32)
