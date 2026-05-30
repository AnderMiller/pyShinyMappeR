from pathlib import Path
from typing import Any

from shiny import ui

import logging
logger = logging.getLogger(__name__)


from Helpers.param import (
    CheckboxParam,
    InputTextParam,
    NumericParam,
    Param,
    SelectParam,
    SliderParam,
    SwitchParam,
)


# TODO:
# add wrapper to give conditional functionality
# need to update base param class
def param_to_ui(module_id: str, param: Param) -> ui.Tag:

    control_id = f"{module_id}__{param.id}"
    logger.info(f"Building UI for {control_id}...") 

    match param:
        case SliderParam():
            return ui.input_slider(
                id=control_id,
                label=param.label,
                value=param.value,
                min=param.min,
                max=param.max,
                step=param.step if param.step is not None else 1,
                ticks=param.ticks,
                width=param.width,
                sep=param.sep,
                pre=param.pre,
                post=param.post,
                animate=param.animate,
                time_format=param.time_format,
                timezone=param.timezone,
                drag_range=param.drag_range,
            )
        case NumericParam():
            return ui.input_numeric(
                id=control_id,
                label=param.label,
                value=param.value,
                update_on=param.update_on,
                min=param.min,
                max=param.max,
                step=param.step if param.step is not None else 1,
                width=param.width,
            )
        case SelectParam():
            return ui.input_select(
                id=control_id,
                label=param.label,
                choices=list(param.choices),
                selected=param.selected,
                multiple=param.multiple,
                width=param.width,
                size=param.size,
            )
        case CheckboxParam():
            return ui.input_checkbox(
                id=control_id,
                label=param.label,
                value=param.value,
                width=param.width,
            )
        case SwitchParam():
            return ui.input_switch(
                id=control_id,
                label=param.label,
                value=param.value,
                width=param.width,
            )
        case InputTextParam():
            return ui.input_text(
                id=control_id,
                label=param.label,
                value=param.value,
                width=param.width,
                placeholder=param.placeholder,
                autocomplete=param.autocomplete,
                spellcheck=param.spellcheck,
                update_on=param.update_on,
            )
        case _:
            raise ValueError(
                f"One of the parameters {(param.id, param.label)} \
                cannot be unpacked by the UI Builder"
            )


def _description_accordion(module_id: str, description: str) -> ui.Tag:
    return ui.tags.div(
        ui.accordion(
            ui.accordion_panel(
                ui.tags.span(
                    "📋️ Description",
                    style="font-weight: 600; letter-spacing: 0.03em;",
                ),
                ui.div(
                    ui.markdown(description),
                    style=(
                        "font-size: 1rem;"
                        "line-height: 1.6;"
                        "padding: 0.5rem 0.5rem;"
                        "border-left: 3px solid #00aa00;"
                        "background: #f5fff5;"
                        "border-radius: 0 6px 6px 0;"
                    ),
                ),
                value="description",
            ),
            id=f"{module_id}__description_accordion",
            open=False,
        ),
        style="margin-bottom: 1rem;",
    )


def dataset_panel(dataset_modules: dict) -> Any:
    if not dataset_modules:
        return ui.nav_panel("Dataset", ui.markdown("_No dataset modules found._"))

    choices = {mid: mod.LABEL for mid, mod in dataset_modules.items()}

    logger.info(f"Dataset Panel: {choices}")

    param_panels = []
    for module_id, mod in dataset_modules.items():
        description = getattr(mod, "DESCRIPTION", None)
        param_panels.append(
            ui.panel_conditional(
                f"input.dataset_select === '{module_id}'",
                _description_accordion(module_id, description)
                if description
                else ui.tags.span(),
                *[param_to_ui(module_id, p) for p in mod.PARAMS],
            )
        )

    return ui.nav_panel(
        "Dataset",
        ui.input_select("dataset_select", "Selected Dataset", choices=choices),
        *param_panels,
    )


def filter_panel(filter_modules: dict) -> Any:
    if not filter_modules:
        return ui.nav_panel("Filter", ui.markdown("_No filter modules found._"))

    choices = {mid: mod.LABEL for mid, mod in filter_modules.items()}

    logger.info(f"Filter Panel: {choices}")


    filter_param_panels = []
    for module_id, mod in filter_modules.items():
        description = getattr(mod, "DESCRIPTION", None)
        filter_param_panels.append(
            ui.panel_conditional(
                f"input.filter_select === '{module_id}'",
                _description_accordion(module_id, description)
                if description
                else ui.tags.span(),
                *[param_to_ui(module_id, p) for p in mod.PARAMS],
            )
        )

    return ui.nav_panel(
        "Filter",
        ui.input_select("filter_select", "Selected Filter Function", choices=choices),
        *filter_param_panels,
    )


def cover_panel(cover_modules: dict) -> Any:
    if not cover_modules:
        return ui.nav_panel("Cover", ui.markdown("_No cover modules found._"))

    choices = {mid: mod.LABEL for mid, mod in cover_modules.items()}

    logger.info(f"Cover Panel: {choices}")

    cover_param_panels = []
    for module_id, mod in cover_modules.items():
        description = getattr(mod, "DESCRIPTION", None)
        cover_param_panels.append(
            ui.panel_conditional(
                f"input.cover_select === '{module_id}'",
                _description_accordion(module_id, description)
                if description
                else ui.tags.span(),
                *[param_to_ui(module_id, p) for p in mod.PARAMS],
            )
        )

    return ui.nav_panel(
        "Cover",
        ui.input_select("cover_select", "Selected Covering Scheme", choices=choices),
        *cover_param_panels,
    )


def cluster_panel(cluster_modules: dict) -> Any:
    if not cluster_modules:
        return ui.nav_panel("Cluster", ui.markdown("_No cluster modules found._"))

    choices = {mid: mod.LABEL for mid, mod in cluster_modules.items()}

    logger.info(f"Cluster Panel: {choices}")

    cluster_param_panels = []
    for module_id, mod in cluster_modules.items():
        description = getattr(mod, "DESCRIPTION", None)
        cluster_param_panels.append(
            ui.panel_conditional(
                f"input.cluster_select === '{module_id}'",
                _description_accordion(module_id, description)
                if description
                else ui.tags.span(),
                *[param_to_ui(module_id, p) for p in mod.PARAMS],
            )
        )

    return ui.nav_panel(
        "Cluster",
        ui.input_select(
            "cluster_select", "Selected Clustering Method", choices=choices
        ),
        *cluster_param_panels,
    )


def visualization_panel(visualization_modules: dict) -> Any:
    if not visualization_modules:
        return ui.nav_panel(
            "Visualization", ui.markdown("_No visualization modules found._")
        )

    choices = {mid: mod.LABEL for mid, mod in visualization_modules.items()}

    print(f"Visualization Panel: {choices}")

    accordion_panels = []
    for module_id, mod in visualization_modules.items():
        description = getattr(mod, "DESCRIPTION", None)
        accordion_panels.append(
            ui.accordion_panel(
                mod.LABEL,
                ui.panel_conditional(
                    f"input.visualization_select.includes('{module_id}')",
                    _description_accordion(module_id, description)
                    if description
                    else ui.tags.span(),
                    *[param_to_ui(module_id, p) for p in mod.PARAMS],
                ),
                value=module_id,
            )
        )

    return ui.nav_panel(
        "Visualization",
        ui.input_checkbox_group(
            "visualization_select",
            "",
            choices=choices,
        ),
        ui.accordion(
            *accordion_panels,
            id="visualization_accordion",
            multiple=True,
            open=False,
        ),
    )


def _help_panel() -> Any:
    readme_path = Path(__file__).parent.parent / "README.md"
    try:
        readme_content = readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        readme_content = "_README.md not found._"
        logger.warning(f"README.md was not found.")
    except Exception as e:
        readme_content = f"_Error loading README.md: {e}_"
        logger.warning(f"Error loading README.md: {e}")

    return ui.nav_panel(
        "❓",
        ui.div(
            ui.markdown(readme_content),
            style=(
                "font-size: 0.95rem;line-height: 1.6;padding: 0.5rem;overflow-y: auto;"
            ),
        ),
    )


def build_sidebar(
    dataset_modules: dict,
    filter_modules: dict,
    cover_modules: dict,
    cluster_modules: dict,
    visualization_modules: dict,
) -> ui.Sidebar:
    logger.info(f"Building Sidebar...")
    return ui.sidebar(
        ui.markdown("# pyShinyMapper"),
        ui.navset_underline(
            dataset_panel(dataset_modules),
            filter_panel(filter_modules),
            cover_panel(cover_modules),
            cluster_panel(cluster_modules),
            visualization_panel(visualization_modules),
            _help_panel(),
        ),
        open="open",
        fillable=True,
        border=True,
        border_radius=True,
        border_color="#000000",
        padding=15,
        bg="#eeeeee",
        position='left'
    )
