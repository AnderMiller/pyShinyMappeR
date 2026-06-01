import matplotlib.pyplot as plt
import networkx as nx
import zen_mapper as zm
from matplotlib.figure import Figure
from zen_mapper.types import MapperResult

from Helpers.param import CheckboxParam, SelectParam, SliderParam
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
    CheckboxParam(
        id="show_labels",
        label="Show Labels",
        value=False,
    ),
    SliderParam(
        id="alpha",
        label="Opacity",
        min=0.1,
        max=1.0,
        value=1.0,
        step=0.05,
    ),
    SelectParam(
        id="layout",
        label="Layout",
        choices=(
            "Kamada-Kawai",
            "Spring",
            "Fruchterman-Reingold",
            "Circular",
            "Random",
            "Shell",
            "Spectral",
            "Planar",
            "Bipartite",
            "Spiral",
        ),
        selected="Kamada-Kawai",
    ),
]


def render_matplotlib(
    ctx: Context, mapper_result: MapperResult, params: dict
) -> Figure:
    G = zm.to_networkx(mapper_result.nerve)

    fig, ax = plt.subplots()

    match params["layout"]:
        case "Kamada-Kawai":
            pos = nx.kamada_kawai_layout(G)
        case "Spring":
            pos = nx.spring_layout(G, seed=42)
        case "Fruchterman-Reingold":
            pos = nx.arf_layout(G, pos=nx.spring_layout(G, seed=42), seed=42)
        case "Circular":
            pos = nx.circular_layout(G)
        case "Random":
            pos = nx.random_layout(G, seed=42)
        case "Shell":
            pos = nx.shell_layout(G)
        case "Spectral":
            pos = nx.spectral_layout(G)
        case "Planar":
            pos = nx.planar_layout(G)
        case "Bipartite":
            pos = nx.bipartite_layout(G, nodes=nx.bipartite.sets(G)[0])
        case "Spiral":
            pos = nx.spiral_layout(G)

    nx.layout
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
