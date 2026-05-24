from typing import Any

import zen_mapper as zm
from sklearn.cluster import AgglomerativeClustering
from zen_mapper.types import Clusterer

from Helpers.param import SliderParam
from Helpers.results import ClustererResult, CovererResult, DatasetResult, FilterResult

LABEL = "Single Linkage"
PARAMS = [
    SliderParam(
        id="distance_threshold",
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
            distance_threshold=params["distance_threshold"],
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
