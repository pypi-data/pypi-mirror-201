from .lib.rw_noise import solve, weights


def run(img, seeds, method):
    weights_h, weights_v = weights(img, method)
    return solve(weights_h, weights_v, seeds)


def fixed(beta):
    return {"name": "fixed", "beta": beta}


def poisson(filter_extent, search_extent=None):
    if search_extent is None:
        search_extent = filter_extent
    return {"name": "poisson",
            "search_extent": search_extent, "filter_extent": filter_extent}


def loupas(filter_extent, search_extent=None):
    if search_extent is None:
        search_extent = filter_extent
    return {"name": "loupas",
            "search_extent": search_extent, "filter_extent": filter_extent}


def ttest(filter_extent, search_extent=None):
    if search_extent is None:
        search_extent = filter_extent
    return {"name": "ttest",
            "search_extent": search_extent, "filter_extent": filter_extent}


def global_gaussian_bian(filter_extent):
    return {"name": "global_gaussian_bian", "filter_extent": filter_extent}


def global_gaussian(filter_extent, search_extent=None):
    if search_extent is None:
        search_extent = filter_extent
    return {"name": "global_gaussian",
            "search_extent": search_extent, "filter_extent": filter_extent}


def variable_gaussian(filter_extent, search_extent=None):
    if search_extent is None:
        search_extent = filter_extent
    return {"name": "variable_gaussian",
            "search_extent": search_extent, "filter_extent": filter_extent}
