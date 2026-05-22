import numpy as np
from sklearn.decomposition import PCA

# Note that PCA centers but does not rescale the data
from Helpers.param import Param

LABEL = "PCA"

# TODO: update depending on the selected output dimension
OUTPUT_DIM = 1

DESCRIPTION = """
### Principle Component Analysis

This function first centers the input data and applies PCA.
"""

PARAMS = [
    Param(
        id="output_dimension",
        type="slider",
        label="Dimenison",
        min=1,
        max=1,
        value=1,
        step=1,
    ),
]


def filter(data: np.ndarray, params: dict) -> np.ndarray:
    filtered_data = PCA(n_components=OUTPUT_DIM).fit_transform(data)
    return filtered_data


def projection_line():
    """
    This should return something that specifies a line
    """
    return None
