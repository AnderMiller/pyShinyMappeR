from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class Param:
    id: str
    type: Literal["slider", "numeric", "select", "checkbox"]
    label: str
    value: Any
    min: float | None = None
    max: float | None = None
    step: float | None = None
    choices: tuple[str, ...] = field(default_factory=tuple)
