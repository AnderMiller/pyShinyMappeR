import plotly.express as pe
from zen_mapper.types import MapperResult

from Helpers.param import SliderParam
from Helpers.results import Context

LABEL = "testingggg"
PARAMS = [
    SliderParam(
        id="dummy_slider",
        label="dummy",
        value=2,
        min=0,
        max=4,
        step=1,
    ),
]


def render_plotly(ctx: Context, mapper_result: MapperResult, params: dict):
    _data = pe.data.iris()

    fig = pe.scatter_3d(
        x=_data.iloc[:, 0], y=_data.iloc[:, 1], z=_data.iloc[:, 2]
    ).update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig
