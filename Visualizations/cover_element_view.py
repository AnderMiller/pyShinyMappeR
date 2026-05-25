import matplotlib.pyplot as plt
from matplotlib import markers
from matplotlib.figure import Figure
from zen_mapper.types import MapperResult

from Helpers.param import SelectParam, SliderParam, SwitchParam
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
        min=0,
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
        min=0.00,
        max=1.0,
        value=0.3,
        step=0.05,
    ),
    SwitchParam(
        id="colormap_is_global",
        label="Color Nodes Globally",
        value=True,
    ),
    SelectParam(
        id="colormap",
        label="Color Map",
        choices=tuple(plt.colormaps()),
        selected="plasma",
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
    num_nodes = len(mapper_result.nodes)

    cover_idx = int(params["selected_cover_element"]) - 1

    assert ctx.dataset is not None
    data = ctx.dataset.data

    # cluster_indices contains the IDs of the nodes in this cover element
    cluster_indices = mapper_result.cover[cover_idx]

    fig, ax = plt.subplots(figsize=(8, 6))

    # background points
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

    # plot each cluster with a different color based on number of nodes.
    cmap = plt.get_cmap(params["colormap"])

    for i, node_id in enumerate(cluster_indices):
        indices = mapper_result.nodes[node_id]
        cluster_color = cmap(i / len(cluster_indices))
        if params["colormap_is_global"]:
            cluster_color = cmap((node_id) / num_nodes)

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
            marker=(i + 3, 0),
        )

    ax.set_aspect("equal")
    ax.set_title(f"Cover Element {cover_idx + 1}")

    # Note: if there are too many clusters, the legend might get messy
    ax.legend(
        title=f"{len(cluster_indices)} Clusters:",
        loc="upper right",
        bbox_to_anchor=(1.5, 1),
    )

    return fig


def update_ui(ctx: Context, mapper_result: MapperResult, mod_id: str):
    n_elements = len(mapper_result.cover)
    # ID as in param_to_ui
    slider_id = f"{mod_id}__selected_cover_element"

    if ctx.ui is not None:
        current_val = ctx.ui.input[slider_id]()

        ctx.ui.update_slider(
            slider_id=slider_id,
            # doing it this way might lead to memory issues
            # depending on if the GC can find it.
            param=SliderParam(
                id="selected_cover_element",
                label="Cover Element",
                value=min(n_elements, current_val),
                min=1,
                max=n_elements,
                step=1,
            ),
        )
