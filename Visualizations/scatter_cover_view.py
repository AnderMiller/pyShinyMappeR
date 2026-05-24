import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from zen_mapper.types import MapperResult

from Helpers.param import SliderParam
from Helpers.results import (
    CovererResult,
    DatasetResult,
    FilterResult,
)

"""
This module requires that the lens function be able to return
the equation of a line on which the original dataset is projected to.
This is straight forward for a theta projection but is more complicated for
something like PCA which auto-centers the dataset.

TODO: Add a supported cover, supported clusterers, etc tags
to the visualization result class.
"""

LABEL = "Scatter With Cover"
PARAMS = [
    SliderParam(
        id="point_size",
        label="Point Size",
        min=1,
        max=50,
        value=10,
        step=1,
    ),
    SliderParam(
        id="alpha",
        label="Opacity",
        min=0.1,
        max=1.0,
        value=0.6,
        step=0.05,
    ),
]
SUPPORTED_FILTER_MOD_IDS = ["theta_projection", "pca_projection"]


def render(
    data_result: DatasetResult,
    filter_result: FilterResult,
    cover_result: CovererResult,
    mapper_result: MapperResult,
    params: dict,
) -> Figure:

    data = data_result.data
    # filtered_data = filter_result.filtered_data
    filter_used = filter_result.label
    fig, ax = plt.subplots()
    ax.scatter(data[:, 0], data[:, 1], s=params["point_size"], alpha=params["alpha"])
    ax.set_aspect("equal")
    ax.set_title(f"Filter Used: {filter_used}")
    return fig
