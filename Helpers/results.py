from dataclasses import dataclass

import numpy as np
from zen_mapper.types import Clusterer, CoverScheme

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


@dataclass
class FilterResult(BasicResult):
    filtered_data: np.ndarray
    line: tuple[str] | None


@dataclass
class CovererResult(BasicResult):
    cover: CoverScheme


@dataclass
class ClustererResult(BasicResult):
    clusterer: Clusterer
