# Visualizations/mapper_graph.py
import matplotlib.pyplot as plt
import networkx as nx
import zen_mapper as zm
from matplotlib.figure import Figure
from zen_mapper.types import MapperResult

from Helpers.param import CheckboxParam, SliderParam
from Helpers.results import Context

LABEL = "Mapper Graph"
PARAMS = [
    SliderParam(
        id="node_size",
        label="Node Size",
        min=1,
        max=1000,
        value=500,
        step=10,
    ),
    CheckboxParam(id="show_labels", label="Show Labels", value=False),
    SliderParam(
        id="alpha",
        label="Opacity",
        min=0.1,
        max=1.0,
        value=1.0,
        step=0.05,
    ),
]


def render_matplotlib(
    ctx: Context, mapper_result: MapperResult, params: dict
) -> Figure:
    G = zm.to_networkx(mapper_result.nerve)

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        ax=ax,
        node_size=params["node_size"],
        alpha=params["alpha"],
        with_labels=params["show_labels"],
    )
    ax.set_title("Mapper Graph")
    ax.set_xlabel(f"{len(mapper_result.nodes)} nodes, {G.number_of_edges()} edges")
    return fig
