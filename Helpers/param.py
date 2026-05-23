# from dataclasses import field
from dataclasses import dataclass
from typing import Any, Literal, Optional


@dataclass(frozen=True)  # state changes should be done using shiny
class Param:
    id: str
    # type: Literal["slider", "numeric", "select", "checkbox"]
    label: str
    # value: Any
    # min: float | None = None
    # max: float | None = None
    # step: float | None = None
    # choices: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SliderParam(Param):
    """
    See `https://shiny.posit.co/py/api/core/ui.input_slider.html`
    """

    # should use kwargs and args and pass into ui in case of updates to shiny
    value: Any
    min: float
    max: float
    step: float
    ticks: bool = False
    width: Optional[str] = None
    sep: str = ","
    pre: Optional[str] = None
    post: Optional[str] = None
    animate: Optional[bool] = False
    time_format: Optional[str] = None
    timezone: Optional[str] = None
    drag_range: Optional[bool] = True


@dataclass(frozen=True)
class NumericParam(Param):
    value: float
    """Initial value."""

    update_on: Literal["change", "blur"] = "change"
    """When should the input value be updated? Options are "change" (default)
    and "blur". Use "change" to update the input immediately whenever the value
    changes. Use "blur"to delay the input update until the input loses focus
    (the user moves away from the input), or when Enter is pressed."""

    min: Optional[float] = None
    """The minimum allowed value."""

    max: Optional[float] = None
    """The maximum allowed value."""

    step: Optional[float] = None
    """Interval to use when stepping between min and max."""

    width: Optional[str] = None
    """The CSS width, e.g. ‘400px’, or ‘100%’"""


@dataclass(frozen=True)
class SelectParam(Param):
    choices: tuple[str] | dict[str, list[str]] | dict[str, dict[str, str]]
    """Either a list of choices or a dictionary mapping choice values to labels.
    Note that if a dictionary is provided, the keys are used as the (input)
    values and the values are labels displayed to the user.
    A dictionary of dictionaries is also supported, and in that case, the
    top-level keys are treated as <optgroup> labels."""

    selected: Optional[str | list[str]] = None
    """The values that should be initially selected, if any."""

    multiple: bool = False
    """Is selection of multiple items allowed?"""

    width: Optional[str] = None
    """The CSS width, e.g. ‘400px’, or ‘100%’"""

    size: Optional[str] = None
    """Number of items to show in the selection box; a larger number will result
    in a taller box. Normally, when multiple=False, a select input will be a
    drop-down list, but when size is set, it will be a box instead."""


@dataclass(frozen=True)
class CheckboxParam(Param):
    value: bool = False
    """Initial value."""

    width: Optional[str] = None
    """The CSS width, e.g. ‘400px’, or ‘100%’"""


@dataclass(frozen=True)
class SwitchParam(Param):
    value: bool = False
    """Initial value."""

    width: Optional[str] = None
    """The CSS width, e.g. ‘400px’, or ‘100%’"""


@dataclass(frozen=True)
class InputTextParam(Param):
    value: str = ""
    """Initial value."""

    width: Optional[str] = None
    """The CSS width, e.g., ‘400px’, or ‘100%’."""

    placeholder: Optional[str] = None
    """A hint as to what can be entered into the control."""

    autocomplete: Optional[str] = "off"
    """Whether to enable browser autocompletion of the text input. If None,
    then it will use the browser’s default behavior. Some values include “
    on”, “off”, “name”, “username”, and “email”. See https://developer.
    mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete to learn more about
    autocomplete’s supported values."""

    spellcheck: Optional[Literal["true", "false"]] = None
    """Whether to enable browser spell checking of the text input
    (default is None). If None, then it will use the browser’s
    default behavior."""

    update_on: Literal["change", "blur"] = "blur"
    """When should the input value be updated? Options are "change" (default)
    and "blur". Use "change" to update the input immediately whenever the value
    changes. Use "blur"to delay the input update until the input loses focus
    (the user moves away from the input), or when Enter is pressed."""
