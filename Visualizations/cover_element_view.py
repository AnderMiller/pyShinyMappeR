import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from zen_mapper.types import MapperResult

from Helpers.param import Param
from Helpers.results import CovererResult, DatasetResult, FilterResult

LABEL = "Cover Element Explorer"
PARAMS = [
    Param(
        id="h_size",
        type="slider",
        label="Highlight Size",
        min=1,
        max=100,
        value=20,
        step=1,
    ),
    Param(
        id="h_alpha",
        type="slider",
        label="Highlight Opacity",
        min=0.1,
        max=1.0,
        value=0.8,
        step=0.05,
    ),
    Param(
        id="bg_size",
        type="slider",
        label="Background Size",
        min=1,
        max=50,
        value=5,
        step=1,
    ),
    Param(
        id="bg_alpha",
        type="slider",
        label="Background Opacity",
        min=0.05,
        max=1.0,
        value=0.3,
        step=0.05,
    ),
    Param(
        id="selected_cover_element",
        type="slider",
        label="Cover Element",
        min=1,
        max=10,
        value=1,
        step=1,
    ),
]


def render(
    data_result: DatasetResult,
    filtered: FilterResult,
    cover: CovererResult,
    nodes: MapperResult,
    params: dict,
) -> Figure:
    num_cover_elements = len(nodes.cover)
    cover_idx = min(int(params["selected_cover_element"]) - 1, num_cover_elements - 1)

    # cluster_indices contains the IDs of the nodes in this cover element
    cluster_indices = nodes.cover[cover_idx]

    fig, ax = plt.subplots(figsize=(8, 6))

    # 1. Background points
    ax.scatter(
        data_result.data[:, 0],
        data_result.data[:, 1],
        s=params["bg_size"],
        alpha=params["bg_alpha"],
        color="lightgray",
        label="Background",
        edgecolors="none",
        zorder=1,
    )

    # 2. Plot each cluster with a different color
    # We use a colormap to generate distinct colors for each node
    cmap = plt.get_cmap("viridis")

    for i, node_id in enumerate(cluster_indices):
        indices = nodes.nodes[node_id]
        cluster_color = cmap((i + 1) / num_cover_elements)  # Cycle through 10 colors

        ax.scatter(
            data_result.data[indices, 0],
            data_result.data[indices, 1],
            s=params["h_size"],
            alpha=params["h_alpha"],
            color=cluster_color,
            label=f"Node {node_id}",
            edgecolors=None,
            linewidths=0.5,
            zorder=2,
        )

    ax.set_aspect("equal")
    ax.set_title(f"Cover Element {cover_idx + 1} ({len(cluster_indices)} clusters)")

    # If there are too many clusters, the legend might get messy
    if len(cluster_indices) < 10:
        ax.legend()

    return fig
