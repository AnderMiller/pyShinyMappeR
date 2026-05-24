import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from Helpers.param import SliderParam
from Helpers.results import CovererResult, DatasetResult, FilterResult

LABEL = "Scatter"
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


def render(
    data_result: DatasetResult,
    filtered: FilterResult,
    cover: CovererResult,
    nodes,
    params,
) -> Figure:
    data = data_result.data
    fig, ax = plt.subplots()
    ax.scatter(data[:, 0], data[:, 1], s=params["point_size"], alpha=params["alpha"])
    ax.set_aspect("equal")
    return fig
