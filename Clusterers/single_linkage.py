import zen_mapper as zm
from sklearn.cluster import AgglomerativeClustering
from zen_mapper.types import Clusterer

from Helpers.param import Param

LABEL = "Single Linkage"
PARAMS = [
    Param(
        id="distance_threshold",
        type="slider",
        label="Distance Threshold",
        min=0.01,
        max=2.0,
        value=0.2,
        step=0.01,
    ),
]


def cluster(params: dict) -> Clusterer:
    return zm.sk_learn(
        AgglomerativeClustering(
            linkage="single",
            n_clusters=None,
            distance_threshold=params["distance_threshold"],
        )
    )
