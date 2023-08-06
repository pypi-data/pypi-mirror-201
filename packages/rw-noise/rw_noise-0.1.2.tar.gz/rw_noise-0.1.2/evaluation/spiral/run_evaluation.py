#!/usr/bin/env python3
import sys
import numpy as np
import csv
import json
import multiprocessing as mp
import data
from os import path, listdir
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util
import math

output = "./result.csv"

methods = [
        util.global_gaussian(2),
        ]

#methods_scalar = [
#        util.ttest(2),
#        util.global_gaussian(2),
#        util.global_gaussian_bian(2),
#        util.variable_gaussian(2),
#        ]


configurations = []

num_tries = 100
for i in range(num_tries):
    random_seed = i

    methods_poisson = [
            util.poisson(2),
            util.loupas(2),
            util.ttest(2),
            util.global_gaussian(2),
            util.global_gaussian_bian(2),
            util.variable_gaussian(2),
            ]
    for beta in util.gen_betas(-3, 5, 5):
        methods_poisson.append(util.fixed(beta))

    for intensity_pow in range(3, 9):
        noise_param = intensity_pow
        int1 = math.pow(2, intensity_pow)
        int2 = math.pow(2, intensity_pow+1)

        def data_fn(seed, int1=int1, int2=int2):
            img = data.gen_image(lambda _: int1, lambda _: int2)
            np.random.seed(seed)
            img = np.random.poisson(img)
            return img.astype(np.float32)

        for method in methods_poisson:
            configurations.append(("poisson", noise_param, method, data_fn, random_seed))

    methods_loupas = [
            util.loupas(2),
            util.poisson(2),
            util.ttest(2),
            util.global_gaussian(2),
            util.global_gaussian_bian(2),
            util.variable_gaussian(2),
            ]
    for beta in util.gen_betas(-3, 5, 5):
        methods_loupas.append(util.fixed(beta))

    for sigma in np.linspace(0.1, 0.5, 10):
        noise_param = sigma
        def data_fn(seed, sigma=sigma):
            img = data.gen_image(lambda _: 0.1, lambda _: 1)
            np.random.seed(seed)
            return data.apply_loupas_noise(img, sigma)

        for method in methods_loupas:
            configurations.append(("loupas", noise_param, method, data_fn, random_seed))

    methods_gaussian = [
            util.global_gaussian(2),
            ]
    for beta in util.gen_betas(-3, 5, 5):
        methods_gaussian.append(util.fixed(beta))

    for sigma in np.linspace(0.1, 1.0, 10):
        noise_param = sigma
        def data_fn(seed, sigma=sigma):
            img = data.gen_image(lambda p: data.tangent(p), lambda p: -data.tangent(p), np.complex64)
            img = util.complex_to_2d(img)
            np.random.seed(seed)
            return data.apply_2d_gaussian_noise(img, sigma)

        for method in methods_gaussian:
            configurations.append(("gaussian2d", noise_param, method, data_fn, random_seed))

mask = data.gen_image(lambda _: 2, lambda _: 1).astype(np.uint32)
num_classes = 2
seeds = data.seed_image()


def process(i, q):
    noise_name, noise_param, method, data_fn, seed = configurations[i]

    img = data_fn(seed)

    def run_with_method(img, method):
        prediction, _ = util.run_rw(img, seeds, method)

        accuracy = np.count_nonzero(prediction == mask)/mask.size
        #util.show_prediction_result(img, prediction, seeds, method["name"])
        row = [seed, 0, noise_name, noise_param, method["name"], json.dumps(method), accuracy]

        q.put(row)

    run_with_method(img, method)


def writer(q):
    with open(output, "a") as fp:
        writer = csv.writer(fp, delimiter=";")
        header = ["seed", "num_labels", "noise_name", "noise_param", "method_name", "method_params", "accuracy"]

        writer.writerow(header)

        print("Started...")
        total = len(configurations)
        z = 0
        while 1:
            row = q.get()
            if row is None:
                break
            writer.writerow(row)
            fp.flush()
            z += 1
            print(f"{z}/{total}")
        print("end!")


n_processes = mp.cpu_count() + 1 # one additional process for the writer
#n_processes = 2 # one additional process for the writer
pool = mp.Pool(n_processes)
manager = mp.Manager()

q = manager.Queue()
#for i in range(0, len(configurations)):
#    process(i, q)
watcher = pool.apply_async(writer, (q,))

params = [(i, q) for i in range(0, len(configurations))]
pool.starmap(process, params)
q.put(None)
watcher.get()
