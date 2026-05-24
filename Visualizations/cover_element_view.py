import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from shiny import reactive
from zen_mapper.types import MapperResult

from Helpers.param import SliderParam
from Helpers.results import Context

LABEL = "Cover Element Explorer"
PARAMS = [
    SliderParam(
        id="h_size",
        label="Highlight Size",
        min=1,
        max=100,
        value=20,
        step=1,
    ),
    SliderParam(
        id="h_alpha",
        label="Highlight Opacity",
        min=0.1,
        max=1.0,
        value=0.8,
        step=0.05,
    ),
    SliderParam(
        id="bg_size",
        label="Background Size",
        min=1,
        max=50,
        value=5,
        step=1,
    ),
    SliderParam(
        id="bg_alpha",
        label="Background Opacity",
        min=0.05,
        max=1.0,
        value=0.3,
        step=0.05,
    ),
    SliderParam(
        id="selected_cover_element",
        label="Cover Element",
        min=1,
        max=10,
        value=1,
        step=1,
    ),
]


def render(ctx: Context, mapper_result: MapperResult, params: dict) -> Figure:
    num_cover_elements = len(mapper_result.cover)

    cover_idx = min(int(params["selected_cover_element"]) - 1, num_cover_elements - 1)

    assert ctx.dataset is not None
    data = ctx.dataset.data

    # cluster_indices contains the IDs of the nodes in this cover element
    cluster_indices = mapper_result.cover[cover_idx]

    fig, ax = plt.subplots(figsize=(8, 6))

    # 1. Background points
    ax.scatter(
        data[:, 0],
        data[:, 1],
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
        indices = mapper_result.nodes[node_id]
        cluster_color = cmap((i + 1) / num_cover_elements)  # Cycle through 10 colors

        ax.scatter(
            data[indices, 0],
            data[indices, 1],
            s=params["h_size"],
            alpha=params["h_alpha"],
            color=cluster_color,
            label=f"Node {node_id}",
            edgecolors=None,
            linewidths=0.5,
            zorder=2,
        )

    ax.set_aspect("equal")
    ax.set_title(
        f"Cover Element {cover_idx + 1} ({len(cluster_indices)} \
        clusters)"
    )

    # If there are too many clusters, the legend might get messy
    if len(cluster_indices) < 10:
        ax.legend()

    return fig


def update_ui(ctx: Context, mapper_result: MapperResult, mod_id: str):
    n_elements = len(mapper_result.cover)
    # ID as in param_to_ui
    slider_id = f"{mod_id}__selected_cover_element"

    if ctx.ui is not None:
        current_val = ctx.ui.input[slider_id]()

        ctx.ui.update_slider(
            slider_id=slider_id,
            param=SliderParam(
                id="selected_cover_element",
                label="Cover Element",
                value=min(n_elements, current_val),
                min=1,
                max=n_elements,
                step=1,
            ),
        )
