import numpy as np
import pygame
import time
import math
import scipy.ndimage
import scipy.spatial
import sklearn.metrics
import matplotlib.pyplot as plt

# Note: you first have to build and install the package in the repository root!

# If you do not want to install, or for local development uncomment the
# following lines to directly use the files in the repository. The shared
# library has to be located in a subfolder "lib".

#import sys
#from os import path
#project_folder_path = path.join(path.dirname(path.abspath(__file__)), "..", "..")
#sys.path.append(project_folder_path)
import rw_noise
from rw_noise import fixed, poisson, ttest, global_gaussian_bian, global_gaussian, variable_gaussian, loupas

run_rw_with_weights = rw_noise.solve
rw_weights = rw_noise.weights
run_rw = rw_noise.run

show_nd_as_color = False

def estimate_scaled_poisson_no_offset_parameter(orig_img):
    gamma_img = 2*np.sqrt(orig_img + 3.0/8)
    alpha = np.var(gamma_img)
    return alpha


def estimate_scaled_poisson_parameters(orig_img):
    img_size = orig_img.shape

    tile_size = 3
    to_remove_y = img_size[0]%tile_size
    to_remove_x = img_size[1]%tile_size

    img = orig_img
    for _ in range(0, to_remove_x):
        img = np.delete(img, (-1), axis=1)
    for _ in range(0, to_remove_y):
        img = np.delete(img, (-1), axis=0)


    sy = img.shape[0]/3
    sx = img.shape[1]/3

    tiles = [tile for slc in np.split(img, sx, axis=1) for tile in np.split(slc, sy, axis=0)]

    means = []
    variances = []

    for tile in tiles:
        vals = tile.flatten()
        med = np.median(vals)
        mean = med
        med_diff = np.abs(vals-med)
        medmed = np.median(med_diff)
        std = 1.4826 * medmed
        variance = std*std

        #mean = np.mean(vals)
        #variance = np.var(vals)

        means.append(mean)
        variances.append(variance)

        means.append(mean)
        variances.append(variance)

    coeff = np.polyfit(means, variances, 1)

    est_alpha = coeff[0]
    est_beta = -coeff[1]/est_alpha

    #poly1d_fn = np.poly1d(coeff)
    #x = np.linspace(0, max(means), 100)
    #plt.plot(x, poly1d_fn(x))
    #plt.scatter(means,variances)
    #plt.show()
    return est_alpha, est_beta


def complex_to_2d(img):
    return np.stack([np.real(img), np.imag(img)], axis=-1).astype(np.float32)

def conv_2d_to_complex(img):
    return img[...,0] + 1j * img[...,1]


def arand(gt, predicted):
    return 1.0-sklearn.metrics.adjusted_rand_score(gt.flatten(), predicted.flatten())

# Compute variance of information
def voi(img1, img2, num_classes):
    n = img1.size
    assert(img2.size == n)
    sum = 0
    for i in range(num_classes):
        ci = i+1
        xi = img1 == ci
        pi = np.count_nonzero(xi)/n
        for j in range(num_classes):
            cj = j+1
            yj = img2 == cj
            qj = np.count_nonzero(yj)/n

            overlap = np.logical_and(xi, yj)
            rij = np.count_nonzero(overlap)/n

            if rij == 0:
                continue
            summand = rij * (math.log2(rij/pi) + math.log2(rij/qj))
            sum += summand
    return -sum

def dice(i1, i2):
    dice_dissimilarity = scipy.spatial.distance.dice(i1.flatten(), i2.flatten())
    dice = 1.0 - dice_dissimilarity
    return dice


def seeds(mask):
    mask_padded = np.pad(mask, 1, constant_values=0)
    distance_padded = scipy.ndimage.morphology.distance_transform_edt(mask_padded)
    distance = distance_padded[1:-1, 1:-1]

    filtered = scipy.ndimage.maximum_filter(distance, size=3)
    #show_image(mask)
    local_maxima = np.logical_and(distance == filtered, distance > 0)
    #show_image(local_maxima)
    return local_maxima.astype(np.uint32)


def labels_from_mask(mask):
    out = np.zeros(mask.shape, dtype=np.uint32)

    max_class = np.max(mask)
    min_class = np.min(mask)

    for c, m in [(i-min_class+1, mask == i) for i in range(min_class, max_class+1)]:
        regions, num_regions = scipy.ndimage.label(m)
        for r in range(1, num_regions+1):
            m = regions == r
            seed_mask = c*seeds(m)
            out = np.maximum(out, seed_mask)

    return out


def normalize_to_u8(im):
    return 255 * (im - im.min()) / (im.max() - im.min())


def gray(im, alpha=None):
    im = normalize_to_u8(im)
    w, h = im.shape
    if alpha:
        c = 4
    else:
        c = 3
    ret = np.empty((w, h, c), dtype=np.uint8)
    ret[:, :, 2] = ret[:, :, 1] = ret[:, :, 0] = im

    if alpha:
        ret[:, :, 3] = alpha

    return ret


def labels_to_img(img, alpha, scaling_factor=1):
    out = labels_to_img_array(img, alpha, scaling_factor)
    surface = pygame.Surface(out.shape[0:2], pygame.SRCALPHA, 32)

    pygame.pixelcopy.array_to_surface(surface, out[:, :, 0:3])

    surface_alpha = np.array(surface.get_view('A'), copy=False)
    surface_alpha[:, :] = out[:, :, 3]
    return surface

def labels_to_img_array(img, alpha, scaling_factor=1):
    img = upsample(img, scaling_factor)
    dy, dx = img.shape
    out = np.zeros((dy, dx, 4), dtype=np.uint8)

    colormap = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 0),
            (1, 0.5, 0),
            (0.5, 0, 1),
            (0, 1, 0.5),
            (0.5, 1, 0),
            (0, 0.5, 1),
            (0.5, 0, 1),
            ]
    num_labels = img.max()
    for label in range(1, num_labels+1):
        colorindex = (label-1) % len(colormap)
        color = np.array(colormap[colorindex])
        colormask = np.einsum("yx,c->yxc", img == label, color)*255
        out[:, :, 0:3] = np.maximum(out[:, :, 0:3], colormask)

    out[:, :, 3] = (img > 0)*alpha
    return out

def composite(img, pimg):
    overlay = img
    image = pimg

    srcRGB = image[...,:3]
    dstRGB = overlay[...,:3]

    # Extract the alpha channels and normalise to range 0..1
    srcA = image[...,3]/255.0
    dstA = overlay[...,3]/255.0

    # Work out resultant alpha channel
    outA = srcA + dstA*(1-srcA)

    # Work out resultant RGB
    outRGB = (srcRGB*srcA[...,np.newaxis] + dstRGB*dstA[...,np.newaxis]*(1-srcA[...,np.newaxis])) / outA[...,np.newaxis]

    # Merge RGB and alpha (scaled back up to 0..255) back into single image
    outRGBA = np.dstack((outRGB,outA*255)).astype(np.uint8)

    return outRGBA


def make_img_surf(img, scaling_factor=1):
    if show_nd_as_color:
        o = np.zeros(list(img.shape[0:2]) + [3])
        if len(img.shape) == 2:
            o = gray(img)
        else:
            for c in range(img.shape[2]):
                o[:, :, c] = normalize_to_u8(img[:, :, c])
    else:
        img = upsample(img, scaling_factor)
        if len(img.shape) > 2:
            img = np.linalg.norm(img, axis=2)
        o = gray(img)

    return pygame.surfarray.make_surface(o)


def upsample(img, scaling_factor):
    return np.repeat(np.repeat(img, scaling_factor, axis=0), scaling_factor, axis=1)


def gen_betas(min_exp, max_exp, steps_per_order_of_magnitude):
    total = (max_exp - min_exp) * steps_per_order_of_magnitude + 1
    return map(lambda e: math.pow(10, e), np.linspace(min_exp, max_exp, total))


def run_interactive_label_loop(img, methods, img_transforms = None, scaling_factor=1):
    pygame.init()
    clock = pygame.time.Clock()

    dy = img.shape[0]
    dx = img.shape[1]
    labels = np.zeros((dy, dx), dtype=np.uint32)
    result = np.zeros((dy, dx), dtype=np.uint32)

    gameDisplay = pygame.display.set_mode((dy * scaling_factor, dx * scaling_factor))
    input_surf = make_img_surf(img, scaling_factor)
    label_surf = labels_to_img(labels, 0, scaling_factor)
    result_surf = labels_to_img(result, 0, scaling_factor)

    end = False
    label_class = 0
    recalculate = False
    some_labels = False
    method = 0
    while not end:
        new_labels = []
        for event in pygame.event.get():
            new_label = False
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.KEYDOWN:
                if pygame.K_F1 <= event.key and event.key <= pygame.K_F12:
                    mn = event.key - pygame.K_F1
                    if mn < len(methods):
                        method = mn
                        recalculate = True
                        pygame.display.set_caption(methods[method]["name"])
                    else:
                        print("Invalid method number")
                elif pygame.K_1 <= event.key and event.key <= pygame.K_9:
                    label_class = event.key - pygame.K_1 + 1
                    new_label = True
            elif event.type == pygame.KEYUP and label_class != 0:
                label_class = 0
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                recalculate = True
            elif event.type == pygame.MOUSEMOTION:
                new_label = True

            if label_class != 0 and new_label:
                new_labels.append((pygame.mouse.get_pos(), label_class))

        if len(new_labels) > 0:
            for pos, c in new_labels:
                y = pos[0]//scaling_factor
                x = pos[1]//scaling_factor
                labels[y, x] = c

                some_labels = True
            label_surf = labels_to_img(labels, 255, scaling_factor)

        if recalculate and some_labels:
            recalculate = False
            before = time.monotonic()
            img_input = img
            if img_transforms is not None:
                img_input = img_transforms[method](img_input)
            map, probs = run_rw(img_input, labels, methods[method])
            after = time.monotonic()
            print(f"Time: {after-before}s")
            result_surf = labels_to_img(map, 50, scaling_factor)
            #for c in range(0, probs.shape[0]):
            #    show_image(probs[c, :, :])



        gameDisplay.blit(input_surf, (0, 0))
        gameDisplay.blit(result_surf, (0, 0))
        gameDisplay.blit(label_surf, (0, 0))

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


def center_point(m):
    mask_padded = np.pad(m, 1, constant_values=0)
    distance_padded = scipy.ndimage.distance_transform_edt(mask_padded)
    distance = distance_padded[1:-1, 1:-1]
    i = np.argmax(distance, keepdims=True)
    p = np.unravel_index(i, distance.shape)
    return p, distance[p]

def generate_initial_seeds(gt, num_classes):
    seeds = np.zeros(gt.shape, dtype=np.uint32)

    for c in range(1, num_classes+1):
        foreground = gt == c
        regions, num_regions = scipy.ndimage.label(foreground)

        for r in range(1, num_regions+1):
            m = regions == r

            center, _ = center_point(m)
            seeds[center] = c

    return seeds

def find_worst_class(gt, predicted, num_classes):
    worst_dice = 1
    worst_class = 0
    for c in range(1, num_classes+1):
        pred = predicted == c
        true = gt == c
        d = dice(pred, true)
        if d < worst_dice:
            worst_dice = d
            worst_class = c

    return worst_class

def select_next_label_position(gt, predicted, num_classes):
    center = None
    worst_dice = 0
    best_class = 0
    worst_class = find_worst_class(gt, predicted, num_classes)

    true_foreground = gt == worst_class
    true_background = gt != worst_class
    predicted_foreground = predicted == worst_class
    predicted_background = predicted != worst_class

    false_background = np.logical_and(true_foreground, predicted_background)
    false_foreground = np.logical_and(true_background, predicted_foreground)

    if false_background.sum() > false_foreground.sum():
        center, _ = center_point(false_background)
    else:
        center, _ = center_point(false_foreground)

    return center

def gen_result_row(gt, predicted, num_classes, n):
    row = {}
    for c in range(1, num_classes+1):
        d = dice(gt == c, predicted == c)
        row[f"dice{c-1}"] = d
    row["voi"] = voi(predicted, gt, num_classes)
    row["arand"] = arand(gt, predicted)
    row["additional_seeds"] = n

    return row


def run_rw_simulation(img, method, gt, num_classes, num_improvements):
    seeds = generate_initial_seeds(gt, num_classes)

    weights_h, weights_v = rw_weights(img, method)

    results = []
    for n in range(num_improvements):
        predicted, _ = run_rw_with_weights(weights_h, weights_v, seeds)

        results.append(gen_result_row(gt, predicted, num_classes, n))

        #show_prediction_result(img, predicted, seeds, f"{method['name']}: after {n} iterations")

        center = select_next_label_position(gt, predicted, num_classes)
        new_seed_class = gt[center]
        seeds[center] = new_seed_class

    predicted, _ = run_rw(img, seeds, method)
    results.append(gen_result_row(gt, predicted, num_classes, num_improvements))

    return results


def run_rw_simulation_prediction_after(img, method, gt, num_classes, num_improvements):
    seeds = generate_initial_seeds(gt, num_classes)

    weights_h, weights_v = rw_weights(img, method)

    for n in range(num_improvements):
        predicted, _ = run_rw_with_weights(weights_h, weights_v, seeds)

        center = select_next_label_position(gt, predicted, num_classes)
        new_seed_class = gt[center]
        seeds[center] = new_seed_class

    predicted, _ = run_rw(img, seeds, method)

    return predicted, seeds


def run_noise_analysis(img, remove_outliers=False):
    pygame.init()
    clock = pygame.time.Clock()

    dy, dx = img.shape

    gameDisplay = pygame.display.set_mode((dy, dx))
    input_surf = pygame.surfarray.make_surface(gray(img))

    end = False
    rect_start = None
    rect_current = None

    def rect():
        left = min(rect_start[0], rect_current[0])
        width = abs(rect_start[0] - rect_current[0])
        top = min(rect_start[1], rect_current[1])
        height = abs(rect_start[1] - rect_current[1])
        return (left, top), (width, height)

    #img = estimate_poisson_params(img)


    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                rect_start = event.pos
                rect_current = rect_start
            elif event.type == pygame.MOUSEMOTION:
                rect_current = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if rect_start is not None:
                    (y, x), (dy, dx) = rect()
                    if dx > 0 and dy > 0:
                        region = img[y:y+dy, x:x+dx]
                        print(region)

                        vals = region.flatten()
                        if remove_outliers:
                            def reject_outliers(data, m = 2.):
                                d = np.abs(data - np.median(data))
                                mdev = np.median(d)
                                s = d/mdev if mdev else 0.
                                return data[s<m]
                            vals = reject_outliers(vals)

                        mean = np.mean(vals)
                        std = np.std(vals)

                        def pdf_gaussian(x, mean, std):
                            return 1/(std * math.sqrt(2 * math.pi)) * math.exp(-0.5 * math.pow((x-mean)/std, 2))
                        def pdf_poisson(x):
                            if mean == 0:
                                return (x==0) * 1
                            return math.exp(x * math.log(mean) - mean - math.lgamma(x+1))


                        print(f"size: {region.shape}")
                        print(f"mean: {mean}, std:{std}")
                        ax = plt.gca()

                        r_min = np.min(vals)
                        r_max = np.max(vals)
                        x = np.linspace(r_min, r_max, num=100)
                        bins = list(map(lambda x: x-0.5, range(math.floor(r_min), math.ceil(r_max)+2)))
                        ax.hist(vals, bins=bins, density=True)
                        ax.plot(x, list(map(lambda x: pdf_gaussian(x, mean, std), x)), label="gaussian estimate")
                        #ax.plot(x, list(map(lambda x: pdf_gaussian(x, mean, math.sqrt(mean)), x)), label="gaussian approx of poisson")
                        ax.plot(x, list(map(pdf_poisson, x)), label="poisson estimate (cont.)")
                        ax.legend()
                        plt.show()


                rect_start = None

        gameDisplay.blit(input_surf, (0, 0))
        if rect_start is not None:
            pos, size = rect()
            pygame.draw.rect(gameDisplay, (255, 0, 0),
                             pygame.Rect(pos, size), width=1)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


def show_image(img):
    dy = img.shape[0]
    dx = img.shape[1]
    gameDisplay = pygame.display.set_mode((dy, dx))
    surf = make_img_surf(img)
    clock = pygame.time.Clock()
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        gameDisplay.blit(surf, (0, 0))

        pygame.display.update()
        clock.tick(60)
    #pygame.quit()


def show_prediction_result(img, classes=None, labels=None, title=None):
    dy = img.shape[0]
    dx = img.shape[1]
    gameDisplay = pygame.display.set_mode((dy, dx))

    input_surf = make_img_surf(img)
    gameDisplay.blit(input_surf, (0, 0))
    if classes is not None:
        result_surf = labels_to_img(classes, 50)
        gameDisplay.blit(result_surf, (0, 0))
    if labels is not None:
        labels_surf = labels_to_img(labels, 255)
        gameDisplay.blit(labels_surf, (0, 0))

    clock = pygame.time.Clock()
    if title is not None:
        pygame.display.set_caption(title)
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
