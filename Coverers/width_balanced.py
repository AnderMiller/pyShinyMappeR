from zen_mapper.cover import Width_Balanced_Cover

from Helpers.param import Param

LABEL = "Width Balanced"
DESCRIPTION = """
There is Some stuff I could add but 

it would look like 

$$
\\Gamma = 2
$$
"""
ACCEPTS_DIM = 1
PARAMS = [
    Param(
        id="n_intervals",
        type="slider",
        label="Intervals",
        min=1,
        max=50,
        value=5,
        step=1,
    ),
    Param(
        id="overlap",
        type="slider",
        label="Overlap %",
        min=0.0,
        max=100.0,
        value=20.0,
        step=0.5,
    ),
]


def cover(params: dict) -> Width_Balanced_Cover:
    return Width_Balanced_Cover(
        n_elements=params["n_intervals"],
        percent_overlap=params["overlap"] / 100,
    )
