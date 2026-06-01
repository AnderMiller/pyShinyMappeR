from logging import getLogger

import numpy as np
import plotly.graph_objects as go
from zen_mapper.types import MapperResult

from Helpers.param import SliderParam
from Helpers.results import (
    Context,
)

logger = getLogger(__name__)

DESCRIPTION = """
This module requires that the lens function be able to return
the equation of a line on which the original dataset is projected to.
This is straight forward for a theta projection but is more complicated for
something like PCA which auto-centers the dataset.
"""

LABEL = "Scatter with Cover/Mapper"
PARAMS = [
    SliderParam(
        id="node_size",
        label="Node Size",
        min=1,
        max=50,
        value=10,
        step=1,
    ),
    SliderParam(
        id="point_size",
        label="Point Size",
        min=1,
        max=25,
        value=5,
        step=1,
    ),
    SliderParam(
        id="alpha",
        label="Cover Opacity",
        min=0,
        max=1.0,
        value=0.90,
        step=0.05,
    ),
    SliderParam(
        id="buffer",
        label="Cover Buffer",
        min=0.05,
        max=1.0,
        value=0.1,
        step=0.05,
    ),
]
SUPPORTED_FILTER_MOD_IDS = [
    "pca_projection",
]


def render_plotly(ctx: Context, mapper_result: MapperResult, params: dict):
    assert ctx.dataset is not None
    assert ctx.filter is not None
    assert ctx.coverer is not None

    data = ctx.dataset.data
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data[:, 0],
            y=data[:, 1],
            mode="markers",
            zorder=-1,
            marker=dict(size=params["point_size"]),
            name=f"{ctx.dataset.label} Data",
        ),
    )
    fig.update_layout(
        title_text=f"{LABEL}",
        yaxis=dict(scaleanchor="x", scaleratio=1),
    )

    # check if we can draw rectangle cover elements
    if (ctx.filter.line is None) or (ctx.coverer.intervals is None):
        logger.error(
            f"The Lens function ({ctx.filter.label}) or Cover Scheme \
            ({ctx.coverer.label}) is not compatible."
        )
        fig.update_layout(
            title_text=f"{LABEL} - The chosen Filter Function or Cover Scheme \
            is not compatible."
        )
        return fig

    # now we can proceed to draw the rectangles
    intervals = ctx.coverer.intervals
    # consider 'point' as the origin
    point = ctx.filter.line.point
    slope_vec = ctx.filter.line.slope_vec

    assert slope_vec is not None
    # rotated 90 degrees
    normal_vec = np.asarray([-slope_vec[1], slope_vec[0]])
    delta = (intervals[-1].right - intervals[0].left) / 2
    buffer = (1 + params["buffer"]) * delta
    left_line_pt = point - buffer * slope_vec
    right_line_pt = point + buffer * slope_vec

    # draw projection line
    fig.add_trace(
        go.Scatter(
            x=[left_line_pt[0], right_line_pt[0]],
            y=[left_line_pt[1], right_line_pt[1]],
            mode="lines",
            line=dict(width=2, color="black", dash="dash"),
            hoverinfo="skip",
            showlegend=True,
            name="Projection Line",
            visible=True,
        )
    )

    # draw cover element rectangles
    for i, erval in enumerate(intervals):
        left_pt = point + erval.left * slope_vec
        right_pt = point + erval.right * slope_vec

        half_width = buffer if i % 2 == 0 else (delta + buffer) / 2

        fig.add_trace(
            go.Scatter(
                x=[
                    (right_pt + half_width * normal_vec)[0],
                    (left_pt + half_width * normal_vec)[0],
                    (left_pt - half_width * normal_vec)[0],
                    (right_pt - half_width * normal_vec)[0],
                    (right_pt + half_width * normal_vec)[0],
                ],
                y=[
                    (right_pt + half_width * normal_vec)[1],
                    (left_pt + half_width * normal_vec)[1],
                    (left_pt - half_width * normal_vec)[1],
                    (right_pt - half_width * normal_vec)[1],
                    (right_pt + half_width * normal_vec)[1],
                ],
                fill="toself",
                mode="lines",
                opacity=params["alpha"],
                hoverinfo="skip",
                showlegend=True,
                legendgroup=f"Cover Element {i}",
                name=f"Element {i + 1}",
            )
        )

    # draw embedded mapper graph
    nodes = mapper_result.nodes
    nerve = mapper_result.nerve
    if len(nodes) == 0:
        raise ValueError("Mapper graph has no nodes")

    node_positions = [np.mean(data[node_indices], axis=0) for node_indices in nodes]
    node_positions = np.array(node_positions)

    # draw edges from nerve[1]
    for node1_id, node2_id in nerve[1]:
        fig.add_trace(
            go.Scatter(
                x=[node_positions[node1_id, 0], node_positions[node2_id, 0]],
                y=[node_positions[node1_id, 1], node_positions[node2_id, 1]],
                mode="lines",
                line=dict(width=2, color="black"),
                hoverinfo="skip",
                showlegend=False,
                legendgroup="Mapper Graph",
            )
        )

    # draw nodes
    fig.add_trace(
        go.Scatter(
            x=node_positions[:, 0],
            y=node_positions[:, 1],
            mode="markers",
            marker=dict(
                size=params["node_size"] + 4,
                color="red",
                line=dict(width=2, color="darkred"),
                symbol="circle",
            ),
            hoverinfo="text",
            text=[f"Node {i}: {len(n)} pts" for i, n in enumerate(nodes)],
            showlegend=True,
            legendgroup="Mapper Graph",
            name="Mapper",
        )
    )

    return fig
