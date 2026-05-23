from dataclasses import dataclass
from typing import Optional

import numpy as np
from zen_mapper.types import Clusterer, CoverScheme

from Helpers.ui_controller import UIController

"""
Server functions should return information necessary to construct
future visualization and other utilities.
"""


# TODO: Update Filter REsults
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
    line: Optional["tuple[str, ...]"] = None


@dataclass
class CovererResult(BasicResult):
    cover: CoverScheme


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
