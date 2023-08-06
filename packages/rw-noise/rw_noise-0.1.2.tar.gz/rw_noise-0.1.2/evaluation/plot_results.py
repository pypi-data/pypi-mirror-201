#! /usr/bin/env python3
import pandas
import matplotlib.pyplot as plt
import numpy as np
import argparse
import seaborn as sns
import os
import json
import math
from matplotlib.ticker import LogFormatterSciNotation

parser = argparse.ArgumentParser()
parser.add_argument("csv", type=str, help="Data to plot", nargs="*")
parser.add_argument("--output", type=str, help="Write figures to specified folder")
args = parser.parse_args()

figure_suffix = ".pdf"
fig_size_x_inches = 10
fig_size_y_inches = 5


def load_data(file):
    all_data = pandas.read_csv(file, delimiter=";")

    all_data.method_params = all_data.method_params.fillna(value="")

    max_scores = ["accuracy"]
    min_scores = ["voi", "arand"]

    max_scores = list(filter(lambda a: a in all_data.columns, max_scores))
    min_scores = list(filter(lambda a: a in all_data.columns, min_scores))

    has_fixed = "fixed" in all_data['method_name'].values
    if has_fixed:
        for s in min_scores:
            all_data = add_virtual_opt_methods(all_data, s, "min", "fixed", "")

        for s in max_scores:
            all_data = add_virtual_opt_methods(all_data, s, "max", "fixed", "")

    has_fixed_scalar = "fixed_scalar" in all_data['method_name'].values
    if has_fixed_scalar:
        for s in min_scores:
            all_data = add_virtual_opt_methods(all_data, s, "min", "fixed_scalar", "scalar_")

        for s in max_scores:
            all_data = add_virtual_opt_methods(all_data, s, "max", "fixed_scalar", "scalar_")

    return all_data


def find_methods(data):
    to_remove = [
            "fixed",
            "fixed_scalar",
            ]

    methods = data[["method_name", "method_params"]].drop_duplicates()
    methods = methods.reset_index()
    for m in to_remove:
        methods = methods.drop(methods[methods["method_name"] == m].index)

    return methods


def line_style(t):
    name = t.method_name
    if "scalar" in name:
        return "--"
    else:
        return "-"

def color(t):
    name = t.method_name
    if "individual_best" in name:
        return [0.5, 0.5, 0.5]
    elif "globally_best" in name:
        return [0.0, 0.0, 0.0]
    elif "variable_gaussian" in name:
        return [0, 0.66, 1]
    elif "global_gaussian" in name:
        if "bian" in name or "ang" in name:
            return [1, 0, 0.3]
        else:
            return [0.33, 0, 1]
    elif "poisson" in name:
        return "green"
    elif "ttest" in name:
        return [1, 0.5, 0]


def method_params_to_json(p):
    if p and isinstance(p, str):
        return json.loads(p)
    else:
        return None


def format_method(t):
    name = t.method_name
    if "individual_best" in name:
        base = "Grady [16] (best $\\beta$ per image)"
    elif "globally_best" in name:
        base = "Grady [16] (globally tuned $\\beta$)"
    elif "variable_gaussian" in name:
        base = "Ours (Gaussian, var. $\\sigma$)"
    elif "global_gaussian" in name:
        if "bian" in name or "ang" in name:
            base = "Bian [4] (Gaussian, const. $\\sigma$)"
        else:
            base = "Ours (Gaussian, const. $\\sigma$)"
    elif "poisson" in name:
        base = "Ours (Poisson)"
    elif "loupas" in name:
        base = "Ours (Loupas)"
    elif "ttest" in name:
        base = "Bian [5] (Gaussian, var. $\\sigma$)"

    if "scalar" in name:
        base += " $||\cdot||_2$"
    return base


def select_noise(data, noise):
    return data.loc[data["noise_name"] == noise]


def select_by_parameter(data, parameter, value):
    def filter_fn(params):
        j = method_params_to_json(params)
        if j:
            p = j.get(parameter)
            if not p is None:
                return p == value
            else:
                return True
        else:
            return True

    return data[data['method_params'].map(filter_fn)]


def select_method_by_name(data, name):
    return data.loc[data["method_name"] == name]


def select_method(data, method):
    return data.loc[(data["method_name"] == method.method_name) & (data["method_params"] == method.method_params)]


def select_subset(data, key, allowed_values):
    return data.loc[data[key].isin(allowed_values)]


def show(figure_name):
    if args.output:
        name = os.path.join(args.output, figure_name + figure_suffix)
        plt.savefig(name, bbox_inches='tight', pad_inches=0)
        plt.cla()
    else:
        plt.show()


def optimal_betas(data, key, opt="max"):
    beta_agg = data.groupby(["seed", "num_labels", "noise_name", "noise_param"])[key]
    if opt == "max":
        return data.loc[beta_agg.idxmax()]
    elif opt == "min":
        return data.loc[beta_agg.idxmin()]
    else:
        raise f"Invalid optimization method: {opt}"


def best_beta_map(data, keys, opt="max"):
    data = select_method_by_name(data, "fixed")

    betas = {}
    fixed = select_method_by_name(data, "fixed")
    for key in keys:
        opt_betas = optimal_betas(fixed, key, opt)
        all_opt_betas = opt_betas.merge(data, on=["seed", "num_labels", "noise_name", "noise_param", "method_name", key], how="inner")
        all_opt_beta_agg = all_opt_betas.groupby(["seed", "num_labels", "noise_name", "noise_param"])
        all_opt_beta_agg = all_opt_beta_agg['method_params_y'].agg(
                weight=lambda col: 1.0/len(col),
                betas=lambda col: list(map(lambda v: json.loads(v)['beta'], iter(col)))
            )

        all_opt_beta_agg.reset_index()
        for _, row in all_opt_beta_agg.iterrows():
            for beta in row.betas:
                if beta not in betas:
                    betas[beta] = 0

                betas[beta] += row['weight']

    return betas


def plot_optimal_beta(data, keys):
    betas = best_beta_map(data, keys)

    ax = plt.gca()
    plt.gcf().set_size_inches(fig_size_x_inches, fig_size_y_inches)
    data = select_method_by_name(data, "fixed")
    all_betas = list(map(lambda v: json.loads(v)['beta'], iter(data['method_params'])))

    ax.set_xscale('log')
    min_beta = min(all_betas)
    max_beta = max(all_betas)
    logbins = np.logspace(np.log10(max(0.00000001, min_beta)),np.log10(max_beta),100)
    ax.hist(betas.keys(), bins=logbins, weights=betas.values())
    ax.set_title("Optimal beta histogram")

    show("best_beta")


def best_beta_by_avg(data, keys, opt="max"):
    data['beta'] = data.apply(lambda row: json.loads(row["method_params"])["beta"], axis=1)

    beta_mean = data.groupby(["beta"]).mean()
    x = beta_mean.index

    y = np.zeros(x.size)
    for key in keys:
        y += beta_mean[key]

    if opt == "max":
        best_i = np.argmax(y)
    elif opt == "min":
        best_i = np.argmin(y)
    else:
        raise f"Invalid optimization method: {opt}"
    return x[best_i]


def best_beta_by_best_count(data, keys):
    best_beta_counts = best_beta_map(a, keys)
    return max(best_beta_counts, key=best_beta_counts.get)


def avg_score_per_beta(data, key):
    data = select_method_by_name(data, "fixed")

    data['beta'] = data.apply(lambda row: json.loads(row["method_params"])["beta"], axis=1)

    beta_mean = data.groupby(["beta"]).mean()
    x = beta_mean.index
    y = beta_mean[key]

    ax = plt.gca()
    plt.gcf().set_size_inches(fig_size_x_inches, fig_size_y_inches)

    ax.set_xscale('log')
    ax.plot(x, y)
    ax.set_title(f"Average {key} per beta")

    show("best_beta_" + str(key))


def box_plot_multi(data, methods, keys):
    fig, axes = plt.subplots(ncols=len(keys), sharey=True)
    fig.set_size_inches(fig_size_x_inches, fig_size_y_inches)
    fig.subplots_adjust(wspace=0)

    methodnames = [format_method(method) for method in methods.itertuples()]

    for ax, key in zip(axes, keys):
        scores = []
        for method in methods.itertuples():
            m = select_method(data, method)

            s = m[key]
            scores.append(s.to_numpy())

        ax.set(xticklabels=methodnames, xlabel=key)
        ax.tick_params(axis='x', rotation=90)
        ax.boxplot(scores, labels=methodnames)

    show("boxplot")


def box_plot_single(data, methods, key):
    methodnames = [format_method(method) for method in methods.itertuples()]

    ax = plt.gca()
    plt.gcf().set_size_inches(fig_size_x_inches, fig_size_y_inches)
    scores = []
    for method in methods.itertuples():
        m = select_method(data, method)

        dice_scores = m[key]
        scores.append(dice_scores.to_numpy())

    ax.set(xticklabels=methodnames)
    ax.tick_params(axis='x', rotation=90)
    ax.boxplot(scores, labels=methodnames)
    ax.set_title(key)

    show("boxplot_"+key)

def plot_key_over_n(data, methods, key, suffix):
    ax = plt.gca()
    plt.gcf().set_size_inches(fig_size_x_inches, fig_size_y_inches)

    x = sorted(data["num_labels"].unique().tolist())
    grouped = data.groupby(["method_name", "method_params", "num_labels"])
    means = grouped.mean().reset_index()
    stddevs = grouped.std().reset_index()

    for method in methods.itertuples():
        m = select_method(means, method)
        s = select_method(stddevs, method)

        y = m[key]
        yerr = s[key]
        #ax.errorbar(x, y, yerr=yerr, label=method, fmt='-', capsize=4, elinewidth=0)
        ax.plot(x, y, label=format_method(method), color=color(method), linestyle=line_style(method))
        #ax.fill_between(x, y-yerr, y+yerr, alpha=0.1)

    ax.set_title(key)
    ax.legend()
    plt.xlabel("# Seed refinements")
    plt.ylabel(f"Mean {key} score")
    ax.set_title(f"Mean {key} score for # of seed refinements")
    plt.yscale('log')
    ax.yaxis.set_minor_formatter(LogFormatterSciNotation(labelOnlyBase=False, minor_thresholds=(2, 0.4)))
    show("mean_over_number_of_refinements_"+key+"_"+suffix)

def plot_median_n_until_below(data, methods, key, suffix, max_val=None, legendpos=None):
    min_val = 0
    if max_val is None:
        g = data
        g = select_subset(g, "method_name", methods["method_name"])
        g = g.groupby(["method_name", "method_params", "num_labels"]).mean()
        g = g.groupby(["method_name", "method_params"]).mean()
        max_val = g.max()[key]

    if legendpos is None:
        legendpos = 'best'


    num_datasets = len(data["seed"].unique())
    median_index = num_datasets//2

    xs = []
    ys = {}
    for method in methods.itertuples():
        ys[method] = []

    d = data
    val_range = np.linspace(max_val, min_val, 100)
    for v in val_range:
        xs.append(v)
        d = d[d[key] < v]

        grouped = d.groupby(["method_name", "method_params", "seed"])
        mins = grouped.min().reset_index()

        for method in methods.itertuples():
            m = select_method(mins, method)
            first_below = m["num_labels"].to_numpy()
            if len(first_below) > median_index:
                median = sorted(first_below)[median_index]
                ys[method].append(median)

    ax = plt.gca()
    plt.gcf().set_size_inches(fig_size_x_inches, fig_size_y_inches)
    for method in methods.itertuples():
        y = ys[method]
        x = xs[:len(y)]
        ax.plot(x, y, label=format_method(method), color=color(method), linestyle=line_style(method))

    plt.xscale('log')
    ax.set_xlim([min(val_range), max(val_range)])
    ax.legend(loc=legendpos)
    plt.xlabel(f"{key} score")
    plt.ylabel("# Seed refinements required")
    ax.set_title(f"Median # of seed refinements until better {key} score")
    show("score_over_median_n_until_below_"+key+"_"+suffix)


def boxplot_n_until_below(data, methods, key, threshold):
    d = data[data[key] < threshold]

    grouped = d.groupby(["method_name", "method_params", "seed"])
    mins = grouped.min().reset_index()
    print(mins)

    methodnames = [format_method(method) for method in methods.itertuples()]

    ax = plt.gca()
    plt.gcf().set_size_inches(fig_size_x_inches, fig_size_y_inches)
    scores = []
    for method in methods.itertuples():
        m = select_method(mins, method)
        first_below = m["num_labels"]

        scores.append(first_below.to_numpy())

    ax.set(xticklabels=methodnames)
    ax.tick_params(axis='x', rotation=90)
    ax.boxplot(scores, labels=methodnames)
    ax.set_title(f"num additional until {key} < {threshold}")
    show("boxplot_below_"+key+str(threshold))

def param_plot_methods_mean_std(data, methods, key, xlabel, title, suffix, sizex=None, sizey=None, legendpos=None, xticklabels=None, invertx=False):

    if sizex is None:
        sizex = fig_size_x_inches
    if sizey is None:
        sizey = fig_size_y_inches

    if legendpos is None:
        legendpos = 'best'

    fig = plt.gcf()
    fig.set_size_inches(sizex, sizey)

    params = sorted(data["noise_param"].unique().tolist())
    grouped = data.groupby(["method_name", "noise_param", "method_params"])
    means = grouped.mean().reset_index()
    stddevs = grouped.std().reset_index()

    ax = plt.gca()
    for method in methods.itertuples():
        m = select_method(means, method)
        std = select_method(stddevs, method)

        x = params
        y = m[key]
        yerr = std[key]
        #ax.errorbar(x, y, yerr=yerr, label=method, fmt='-', capsize=4, elinewidth=0)
        ax.plot(x, y, label=format_method(method), color=color(method), linestyle=line_style(method))
        ax.fill_between(x, y-yerr, y+yerr, alpha=0.1, color=color(method))

    if xticklabels is not None:
        ax.set_xticklabels(xticklabels)
    if invertx:
        ax.invert_xaxis()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(key)

    ax.legend(loc=legendpos)
    show("noise_vs_" + str(key) + "_" + suffix)


def param_plot_methods_median_min_max(data, methods, keys):

    fig, axes = plt.subplots(ncols=len(keys), sharey=True)
    if len(keys) == 1:
        axes = [axes]
    fig.set_size_inches(fig_size_x_inches, fig_size_y_inches)
    fig.subplots_adjust(wspace=0)

    params = sorted(data["noise_param"].unique().tolist())
    grouped = data.groupby(["method_name", "noise_param", "method_params"])
    medians = grouped.median().reset_index()
    mins = grouped.min().reset_index()
    maxs = grouped.max().reset_index()

    for ax, key in zip(axes, keys):
        for method in methods.itertuples():
            med = select_method(medians, method)
            min_e = select_method(mins, method)[key].to_numpy()
            max_e = select_method(maxs, method)[key].to_numpy()

            x = params
            y = med[key]
            #ax.errorbar(x, y, yerr=yerr, label=method, fmt='-', capsize=4, elinewidth=0)
            ax.plot(x, y, label=format_method(method))
            ax.fill_between(x, min_e, max_e, alpha=0.1)

    ax.legend()
    show("noise_vs_" + str(keys))


def add_virtual_opt_methods(all_data, s, opt, method_name, name_suffix):
    fixed = all_data.loc[(all_data["method_name"] == method_name)]
    best_betas = optimal_betas(fixed, s, opt)
    best_betas["method_name"] = "individual_best_beta_" + name_suffix + s
    best_betas["method_params"] = "{}"

    all_data = all_data.append(best_betas)

    first_data = fixed[fixed["num_labels"] == 0]
    globally_best_beta = best_beta_by_avg(first_data, [s], opt)
    print(f"Selected best beta {globally_best_beta} for {s}")
    globally_best_beta_scores = select_by_parameter(fixed, "beta", globally_best_beta)
    globally_best_beta_scores["method_name"] = "globally_best_beta_" + name_suffix + s

    all_data = all_data.append(globally_best_beta_scores)

    return all_data

def without_methods(methods, to_remove):
    methods = methods.copy()
    for m in to_remove:
        methods = methods.drop(methods[methods["method_name"] == m].index)
    return methods


def find_with_best(data, key, noise_name, noise_param_min, noise_param_max, seed, num_labels, modifier=None):
    d = data
    d = d[d["num_labels"] == num_labels]
    d = d[d["noise_name"] == noise_name]
    d = d[d["noise_param"] >= noise_param_min]
    d = d[d["noise_param"] <= noise_param_max]
    d = d[d["seed"] == seed]

    if modifier is not None:
        method_name_selector = "individual_best_beta_" + modifier + "_" + key
        fixed_selector = "fixed_" + modifier
    else:
        method_name_selector = "individual_best_beta_" + key
        fixed_selector = "fixed"

    best = d[d["method_name"] == method_name_selector]
    print(best[key])
    best_key_val = float(best[key])

    fixed = d[d["method_name"] == fixed_selector]
    return fixed[fixed[key] == best_key_val]


def spiral_data_plots():
    all_data = load_data("spiral/result.csv")

    seed = 4
    print(find_with_best(all_data, "accuracy", "poisson", 5, 5, seed, 0))
    print(find_with_best(all_data, "accuracy", "loupas", 0.18, 0.19, seed, 0))
    print(find_with_best(all_data, "accuracy", "gaussian2d", 0.3, 0.3, seed, 0))

    poisson_data = select_noise(all_data, "poisson")
    poisson_methods = find_methods(poisson_data)
    poisson_methods = without_methods(poisson_methods, ["global_gaussian"])
    sizex = 7
    sizey = 5
    param_plot_methods_mean_std(poisson_data, poisson_methods, "accuracy", "$\\lambda_0/\\lambda_1$", "Poisson Noise", "poisson", sizex, sizey, 'lower left', [f'{int(math.pow(2, i))}/{int(math.pow(2, i+1))}' for i in range(2, 9)], True)

    loupas_data = select_noise(all_data, "loupas")
    loupas_methods = find_methods(loupas_data)
    loupas_methods = without_methods(loupas_methods, ["global_gaussian"])
    param_plot_methods_mean_std(loupas_data, loupas_methods, "accuracy", "$\\sigma$", "Loupas Noise", "loupas", sizex, sizey)

    gaussian2d_data = select_noise(all_data, "gaussian2d")
    gaussian2d_methods = find_methods(gaussian2d_data)
    param_plot_methods_mean_std(gaussian2d_data, gaussian2d_methods, "accuracy", "$\\sigma$", "2D Gaussian Noise", "gaussian2d", sizex, sizey)


def larvae_data():

    all_data = load_data("fim/result.csv")
    methods = find_methods(all_data)
    methods = without_methods(methods, ["global_gaussian"])
    voi_methods = without_methods(methods, ["individual_best_beta_arand", "globally_best_beta_arand", "individual_best_beta_scalar_arand", "globally_best_beta_scalar_arand"])
    arand_methods = without_methods(methods, ["individual_best_beta_voi", "globally_best_beta_voi", "individual_best_beta_scalar_voi", "globally_best_beta_scalar_voi"])

    seed = 3
    print(find_with_best(all_data, "voi", "fim", 0, 0, seed, 0))

    plot_key_over_n(all_data, voi_methods, "voi", "fim")
    plot_median_n_until_below(all_data, voi_methods, "voi", "fim", legendpos="upper center")

    plot_key_over_n(all_data, arand_methods, "arand", "fim")
    plot_median_n_until_below(all_data, arand_methods, "arand", "fim", legendpos="upper center")


def mri_data():
    all_data = load_data("fastmri/result.csv")
    methods = find_methods(all_data)
    methods = without_methods(methods, ["variable_gaussian_scalar"])
    voi_methods = without_methods(methods, ["individual_best_beta_arand", "globally_best_beta_arand", "individual_best_beta_scalar_arand", "globally_best_beta_scalar_arand", ])
    arand_methods = without_methods(methods, ["individual_best_beta_voi", "globally_best_beta_voi", "individual_best_beta_scalar_voi", "globally_best_beta_scalar_voi"])

    seed = 90
    num_labels = 10
    print(find_with_best(all_data, "voi", "mri", 0, 0, seed, num_labels))
    print(find_with_best(all_data, "voi", "mri", 0, 0, seed, num_labels, "scalar"))

    plot_key_over_n(all_data, voi_methods, "voi", "mri")
    plot_median_n_until_below(all_data, voi_methods, "voi", "mri")

    plot_key_over_n(all_data, arand_methods, "arand", "mri")
    plot_median_n_until_below(all_data, arand_methods, "arand", "mri")


larvae_data()
mri_data()
spiral_data_plots()
