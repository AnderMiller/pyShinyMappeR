from dataclasses import dataclass
from logging import getLogger
from typing import Any, List, Optional

import numpy as np
from pandas import Interval
from zen_mapper.types import Clusterer

from Helpers.ui_controller import UIController

logger = getLogger(__name__)

"""
Server functions should return information necessary to construct
future visualization and other utilities.
"""


@dataclass
class ProjectionLine:
    point: np.ndarray
    """The point is considered the origin in the filtered space."""
    slope_vec: Optional[np.ndarray]
    """The slope vector is the positive direction in the filter space (1D)."""

    def slope(self):
        if not self.slope_vec:
            logger.error("Projection line has no slope vector provided.")
            return np.inf
        if self.slope_vec is not None:
            if self.slope_vec[0] == 0:
                logger.error("DIVIDEBYZERO: slope vector has dx==0...")

                return np.inf
            return self.slope_vec[-1] / self.slope_vec[0]


@dataclass
class BasicResult:
    params: dict
    module_id: str
    modules: dict
    label: str


@dataclass
class DatasetResult(BasicResult):
    data: np.ndarray

    def shape(self):
        return np.shape(self.data)


@dataclass
class FilterResult(BasicResult):
    filtered_data: np.ndarray
    line: Optional[ProjectionLine]
    output_dim: Optional["int"] = None


@dataclass
class CovererResult(BasicResult):
    cover: List[Any]
    """Cover is a list[list[int,...]] of filter-data index values.
    Each inner list is a cover element."""
    intervals: Optional[list[Interval]] = None


@dataclass
class ClustererResult(BasicResult):
    clusterer: Clusterer


# Do not put hard to compute things inside of context.
@dataclass
class Context:
    dataset: Optional["DatasetResult"] = None
    filter: Optional["FilterResult"] = None
    coverer: Optional["CovererResult"] = None
    clusterer: Optional["ClustererResult"] = None
    ui: Optional["UIController"] = None

    def __post_init__(self):
        # TODO: add checks or flags
        # for example:
        pass
