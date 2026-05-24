from typing import Any

import numpy as np

from Helpers.param import SliderParam
from Helpers.results import DatasetResult, FilterResult

LABEL = "$\\theta$-Projection"
OUTPUT_DIM = 1

DESCRIPTION = """
### $ \\theta$-Projection

This filter function projects 2D-data to $x$-axis rotated $\\theta$ degrees
counter-clockwise.
"""

PARAMS = [
    SliderParam(
        id="theta_proj",
        label="Projection $( \\theta ^\\circ ) $ ",
        min=0.0,
        max=180,
        value=0,
        step=1,
    ),
]


def filter(data: np.ndarray, params: dict) -> np.ndarray:
    filtered_data = (
        np.cos(np.pi * params["theta_proj"] / 180) * data[:, 0]
        + np.sin(np.pi * params["theta_proj"] / 180) * data[:, 1]
    )
    return filtered_data


def projection_line():
    return None


def result(dataset: DatasetResult, params: dict, modules: Any, module_id: Any):
    return FilterResult(
        params=params,
        modules=modules,
        module_id=module_id,
        label=LABEL,
        filtered_data=filter(data=dataset.data, params=params),
        line=projection_line(),
    )
