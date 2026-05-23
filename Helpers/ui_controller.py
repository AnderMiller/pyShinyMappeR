from dataclasses import dataclass
from typing import Any

from shiny import ui

from Helpers.param import (
    CheckboxParam,
    InputTextParam,
    NumericParam,
    SelectParam,
    SliderParam,
    SwitchParam,
)


@dataclass
class UIController:
    session: Any
    input: Any

    def update_slider(self, slider_id: str, param: SliderParam):
        ui.update_slider(
            id=slider_id,
            value=param.value,
            min=param.min,
            max=param.max,
            step=param.step,
            time_format=param.time_format,
            timezone=param.timezone,
            session=self.session,
        )

    def update_numeric(self, numeric_id: str, param: NumericParam):
        ui.update_numeric(
            id=numeric_id,
            value=param.value,
            min=param.min,
            max=param.max,
            step=param.step,
            session=self.session,
        )

    def update_select(self, select_id: str, param: SelectParam):
        # typechecker is mad because shiny uses a type that doesnt exist
        # :/
        ui.update_select(
            id=select_id,
            choices=param.choices,
            selected=param.selected,
            session=self.session,
        )

    def update_checkbox(self, checkbox_id: str, param: CheckboxParam):
        ui.update_checkbox(
            id=checkbox_id, label=param.label, value=param.value, session=self.session
        )

    def update_switch(self, switch_id: str, param: SwitchParam):
        ui.update_switch(
            id=switch_id, label=param.label, value=param.value, session=self.session
        )

    def update_input_text(self, input_text_id: str, param: InputTextParam):
        ui.update_text(
            id=input_text_id,
            label=param.label,
            value=param.value,
            placeholder=param.placeholder,
            session=self.session,
        )
