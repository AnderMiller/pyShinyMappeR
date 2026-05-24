from typing import Any

import zen_mapper as zm
from sklearn.cluster import DBSCAN
from zen_mapper.types import Clusterer

from Helpers.param import SelectParam, SliderParam
from Helpers.results import ClustererResult, CovererResult, DatasetResult, FilterResult

LABEL = "DBSCAN"
PARAMS = [
    SliderParam(
        id="eps",
        label="$\\epsilon$",
        min=0.01,
        max=2.0,
        value=0.2,
        step=0.01,
    ),
    SliderParam(
        id="min_samples",
        label="Min Samples",
        min=1,
        max=25,
        value=5,
        step=1,
    ),
    SelectParam(
        id="metric",
        label="Metric",
        choices=(
            "chebyshev",
            "euclidean",
            "cityblock",
            # -- The above are valid for kd_tree
            "braycurtis",
            "canberra",
            "dice",
            "hamming",
            "jaccard",
            "rogerstanimoto",
            "russellrao",
            "sokalsneath",
            # # --- The below are NOT valid for ball_tree
            "correlation",
            "cosine",
            "sqeuclidean",
            "yule",
            # # --- not valid for auto
            # "mahalanobis",
            # "jensenshannon",
            # "minkowski",
            # "seuclidean",
            # "matching",
        ),
        selected="euclidean",
    ),
    SelectParam(
        id="algorithm",
        label="Algorithm (Locked to Auto)",
        choices=(
            "auto",
            # "ball_tree",
            # "brute",
            # "kd_tree",
            ### -----
            ### The algorithm option is disabled since it is
            ### not super important.
            ### If a user wants to include it they can uncomment this
        ),
        selected="auto",
    ),
    SliderParam(
        id="leaf_size",
        label="Leaf Size (algorithm option)",
        value=30,
        min=1,
        max=100,
        step=1,
    ),
]


def cluster(params: dict) -> Clusterer:
    return zm.sk_learn(
        DBSCAN(
            eps=params["eps"],
            min_samples=params["min_samples"],
            metric=params["metric"],
            algorithm=params["algorithm"],
            leaf_size=params["leaf_size"],
        )
    )


def result(
    data: DatasetResult,
    filtered: FilterResult,
    cover: CovererResult,
    params: dict,
    modules: Any,
    module_id: Any,
):
    return ClustererResult(
        params=params,
        modules=modules,
        module_id=module_id,
        label=LABEL,
        clusterer=cluster(params=params),
    )
