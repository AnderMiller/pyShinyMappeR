from typing import Any

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


def cover(params: dict) -> Width_Balanced_Cover:
    return Width_Balanced_Cover(
        n_elements=params["n_intervals"],
        percent_overlap=params["overlap"] / 100,
    )


def result(
    data: DatasetResult,
    filtered: FilterResult,
    params: dict,
    modules: Any,
    module_id: Any,
):
    return CovererResult(
        params=params,
        module_id=module_id,
        modules=modules,
        label=LABEL,
        cover=cover(params),
    )
