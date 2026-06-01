from typing import Any

import numpy as np
from sklearn.decomposition import PCA

# Note that PCA centers but does not rescale the data
from Helpers.param import SliderParam
from Helpers.results import DatasetResult, FilterResult, ProjectionLine

LABEL = "PCA"
OUTPUT_DIM = 1
# this is required but is not really used


# TODO: update depending on the selected output dimension
DESCRIPTION = """
### Principle Component Analysis

This function first centers the input data and applies PCA.
"""

PARAMS = [
    SliderParam(
        id="output_dimension",
        label="Dimenison",
        min=1,
        max=1,
        value=1,
        step=1,
    ),
]


def filter(data: np.ndarray, params: dict) -> tuple[Any, ProjectionLine]:
    pca = PCA(n_components=int(params["output_dimension"]))
    filtered_data = pca.fit_transform(data)
    assert pca.components_ is not None

    # tuple of (point, slope-vector)
    projection_line = ProjectionLine(point=pca.mean_, slope_vec=pca.components_[0])

    return filtered_data, projection_line


def result(dataset: DatasetResult, params: dict, modules: Any, module_id: Any):
    filtered_data, projection_line = filter(data=dataset.data, params=params)
    return FilterResult(
        params=params,
        module_id=module_id,
        modules=modules,
        label=LABEL,
        filtered_data=filtered_data,
        line=projection_line,
        output_dim=int(params["output_dimension"]),
    )
