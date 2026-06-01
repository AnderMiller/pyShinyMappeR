from logging import getLogger

import numpy as np
import plotly.graph_objects as go
from zen_mapper.types import MapperResult

from Helpers.param import SliderParam
from Helpers.results import (
    Context,
)

logger = getLogger(__name__)

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
        min=0,
        max=1.0,
        value=0.90,
        step=0.05,
    ),
    SliderParam(
        id="buffer",
        label="Buffer Ratio",
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
        go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers"),
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

    # draw the line
    fig.add_shape(
        type="line",
        x0=left_line_pt[0],
        y0=left_line_pt[1],
        x1=right_line_pt[0],
        y1=right_line_pt[1],
    )

    # now we can draw the rectangles
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
            )
        )

    return fig
