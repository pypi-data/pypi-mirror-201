#!/usr/bin/env python3
import sys
import numpy as np
import csv
import json
import re
import multiprocessing as mp
import data
from os import path, listdir
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import util

output = "./result.csv"
num_label_improvements = 50

files = data.data_files()

methods = [
        util.global_gaussian(2),
        ]

methods_scalar = [
        util.ttest(2),
        util.global_gaussian(2),
        util.global_gaussian_bian(2),
        util.variable_gaussian(2),
        ]


for beta in util.gen_betas(0, 5, 5):
    methods.append(util.fixed(beta))
    methods_scalar.append(util.fixed(beta))


def process(i, q):
    img, mask, num_classes = data.load_file(files, i)

    def run_with_method(img, method, suffix):
        results = util.run_rw_simulation(img, method, mask, num_classes, num_label_improvements)
        method_name = method["name"]+suffix

        for r in results:
            row = [i, r["additional_seeds"], "mri", 0, method_name, json.dumps(method), r["voi"], r["arand"]]

            for c in range(num_classes):
                row.append(r[f"dice{c}"])

            q.put(row)

    img_scalar = np.linalg.norm(img, axis=2)
    for method in methods_scalar:
        run_with_method(img_scalar, method, "_scalar")

    for method in methods:
        run_with_method(img, method, "")


def writer(q):
    with open(output, "a") as fp:
        writer = csv.writer(fp, delimiter=";")
        header = ["seed", "num_labels", "noise_name", "noise_param", "method_name", "method_params", "voi", "arand"]
        for c in range(0, data.expected_num_classes):
            header.append(f"dice{c}")

        writer.writerow(header)

        print("Started...")
        total = (len(methods) + len(methods_scalar)) * len(files) * (num_label_improvements+1)
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
#for i in range(1, len(files)):
#    process(i, q)
watcher = pool.apply_async(writer, (q,))

params = [(i, q) for i in range(0, len(files))]
pool.starmap(process, params)
q.put(None)
watcher.get()
