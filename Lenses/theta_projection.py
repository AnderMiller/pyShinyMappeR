import numpy as np

from Helpers.param import Param

LABEL = "$\\theta$-Projection"
OUTPUT_DIM = 1

DESCRIPTION = """
### $ \\theta$-Projection

This filter function projects 2D-data to $x$-axis rotated $\\theta$ degrees
counter-clockwise.
"""

PARAMS = [
    Param(
        id="theta_proj",
        type="slider",
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
