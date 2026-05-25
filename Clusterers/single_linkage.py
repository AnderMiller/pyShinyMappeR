from typing import Any

import zen_mapper as zm
from sklearn.cluster import AgglomerativeClustering
from zen_mapper.types import Clusterer, MapperResult

from Helpers.param import SelectParam, SliderParam, SwitchParam
from Helpers.results import (
    ClustererResult,
    Context,
    CovererResult,
    DatasetResult,
    FilterResult,
)

LABEL = "Single Linkage"
DESCRIPTION = """
Metric used to compute the linkage. Can be “euclidean”, “l1”, “l2”,
“manhattan”, “cosine”, or “precomputed”.
If linkage is “ward”, only “euclidean” is accepted.
"""
PARAMS = [
    SliderParam(
        id="distance_threshold",
        label="Distance Threshold",
        min=0.01,
        max=2.0,
        value=0.2,
        step=0.01,
    ),
    SwitchParam(
        id="use_n_clusters",
        label="N Clusters",
        value=False,
    ),
    SliderParam(
        id="n_clusters",
        label="N",
        value=2,
        min=2,
        max=20,
        step=1,
    ),
    SelectParam(
        id="linkage_method",
        label="Linkage Method",
        choices=(
            "ward",
            "complete",
            "average",
            "single",
        ),
        selected="single",
    ),
    SelectParam(
        id="linkage_metric",
        label="Metric",
        choices=(
            "euclidean",
            "l1",
            "l2",
            "manhattan",
            "cosine",
        ),
    ),
]


def update_ui(ctx: Context, mapper_result: MapperResult, mod_id: str):
    linkage_id = f"{mod_id}__linkage_method"
    metric_id = f"{mod_id}__linkage_metric"

    # make euclidean the only option for ward

    if ctx.ui is not None:
        if ctx.ui.input[linkage_id]() == "ward":
            ctx.ui.update_select(
                select_id=metric_id,
                param=SelectParam(
                    id="linkage_metric",
                    label="Metric",
                    choices=("euclidean",),
                    selected="euclidean",
                ),
            )
        else:
            ctx.ui.update_select(
                select_id=metric_id,
                param=SelectParam(
                    id="linkage_metric",
                    label="Metric",
                    choices=(
                        "euclidean",
                        "l1",
                        "l2",
                        "manhattan",
                        "cosine",
                    ),
                    selected=ctx.ui.input[metric_id](),
                ),
            )


def cluster(params: dict) -> Clusterer:

    # only one of n_clusters or distance_threshold can be not None
    n_clusters = None
    dist_thresh = params["distance_threshold"]
    if params["use_n_clusters"]:
        n_clusters = int(params["n_clusters"])
        dist_thresh = None

    # also make sure that if we are passed 'ward' we use 'euclidean'
    linkage_metric = params["linkage_metric"]
    if params["linkage_method"] == "ward":
        linkage_metric = "euclidean"

    return zm.sk_learn(
        AgglomerativeClustering(
            linkage=params["linkage_method"],
            distance_threshold=dist_thresh,
            n_clusters=n_clusters,
            metric=linkage_metric,
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
