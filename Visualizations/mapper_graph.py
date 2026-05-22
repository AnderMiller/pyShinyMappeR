# Visualizations/mapper_graph.py
import matplotlib.pyplot as plt
import networkx as nx
import zen_mapper as zm
from matplotlib.figure import Figure
from zen_mapper.types import MapperResult

from Helpers.param import Param

LABEL = "Mapper Graph"
PARAMS = [
    Param(
        id="node_size",
        type="slider",
        label="Node Size",
        min=10,
        max=500,
        value=200,
        step=10,
    ),
    Param(
        id="alpha",
        type="slider",
        label="Opacity",
        min=0.1,
        max=1.0,
        value=1.0,
        step=0.05,
    ),
]


def render(data, filtered, cover, result: MapperResult, params) -> Figure:
    G = zm.to_networkx(result.nerve)

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        ax=ax,
        node_size=params["node_size"],
        alpha=params["alpha"],
        with_labels=False,
    )
    ax.set_title("Mapper Graph")
    ax.set_xlabel(f"{len(result.nodes)} nodes, {G.number_of_edges()} edges")
    print(cover.__dict__)
    print("###########")
    print(filtered)
    return fig
