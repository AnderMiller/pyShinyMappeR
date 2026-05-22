import zen_mapper as zm
from sklearn.cluster import DBSCAN
from zen_mapper.types import Clusterer

from Helpers.param import Param

LABEL = "DBSCAN"
PARAMS = [
    Param(
        id="eps",
        type="slider",
        label="$\\epsilon$",
        min=0.01,
        max=2.0,
        value=0.2,
        step=0.01,
    ),
    Param(
        id="min_samples",
        type="slider",
        label="Min Samples",
        min=1,
        max=25,
        value=5,
    ),
    Param(
        id="metric",
        type="select",
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
        value="euclidean",
    ),
    Param(
        id="algorithm",
        type="select",
        label="Algorithm",
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
        value="auto",
    ),
    Param(
        id="leaf_size",
        type="slider",
        label="Leaf Size",
        value=30,
        min=1,
        max=100,
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
