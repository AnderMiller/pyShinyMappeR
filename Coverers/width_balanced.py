from typing import Any, Tuple

import numpy as np
from pandas import Interval
from zen_mapper.cover import Width_Balanced_Cover

from Helpers.param import SliderParam
from Helpers.results import CovererResult, DatasetResult, FilterResult

LABEL = "Width Balanced"
DESCRIPTION = """
There is Some stuff I could add but

it would look like

$$
\\Gamma = 2
$$
"""
ACCEPTS_DIM = 1
PARAMS = [
    SliderParam(
        id="n_intervals",
        label="Intervals",
        min=1,
        max=50,
        value=5,
        step=1,
    ),
    SliderParam(
        id="overlap",
        label="Overlap %",
        min=0.0,
        max=100.0,
        value=20.0,
        step=0.5,
    ),
]


def cover(filtered_data, params: dict) -> Tuple[Any, list[Interval]]:
    cover_scheme = Width_Balanced_Cover(
        n_elements=params["n_intervals"],
        percent_overlap=params["overlap"] / 100,
    )
    cover_elements = list(map(np.asarray, cover_scheme(filtered_data)))
    # need to call cover_scheme to create widths
    width = cover_scheme.width
    centers = cover_scheme.centers
    intervals = list()

    for i in range(params["n_intervals"]):
        intervals.append(
            Interval(
                left=centers[i][0] - width[0] / 2, right=centers[i][0] + width[0] / 2
            )
        )

    return cover_elements, intervals


def result(
    data: DatasetResult,
    filtered: FilterResult,
    params: dict,
    modules: Any,
    module_id: Any,
):
    cover_elements, intervals = cover(filtered.filtered_data, params)
    return CovererResult(
        params=params,
        module_id=module_id,
        modules=modules,
        label=LABEL,
        cover=cover_elements,
        intervals=intervals,
    )
