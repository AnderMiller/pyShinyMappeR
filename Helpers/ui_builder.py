from pathlib import Path

from shiny import ui

from Helpers.param import Param


def param_to_ui(module_id: str, param: Param) -> ui.Tag:
    control_id = f"{module_id}__{param.id}"

    match param.type:
        case "slider":
            return ui.input_slider(
                control_id,
                param.label,
                min=param.min,
                max=param.max,
                value=param.value,
                step=param.step if param.step is not None else 1,
            )
        case "numeric":
            return ui.input_numeric(
                control_id,
                param.label,
                value=param.value,
                min=param.min,
                max=param.max,
                step=param.step if param.step is not None else 1,
            )
        case "select":
            return ui.input_select(
                control_id,
                param.label,
                choices=list(param.choices),
                selected=param.value,
            )
        case "checkbox":
            return ui.input_checkbox(
                control_id,
                param.label,
                value=param.value,
            )
        case _:
            raise ValueError(f"Unknown param type '{param.type}' in param '{param.id}'")


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


def dataset_panel(dataset_modules: dict) -> ui.Tag:
    if not dataset_modules:
        return ui.nav_panel("Dataset", ui.markdown("_No dataset modules found._"))

    choices = {mid: mod.LABEL for mid, mod in dataset_modules.items()}

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


def filter_panel(filter_modules: dict) -> ui.Tag:
    if not filter_modules:
        return ui.nav_panel("Filter", ui.markdown("_No filter modules found._"))

    choices = {mid: mod.LABEL for mid, mod in filter_modules.items()}

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


def cover_panel(cover_modules: dict) -> ui.Tag:
    if not cover_modules:
        return ui.nav_panel("Cover", ui.markdown("_No cover modules found._"))

    choices = {mid: mod.LABEL for mid, mod in cover_modules.items()}

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


def cluster_panel(cluster_modules: dict) -> ui.Tag:
    if not cluster_modules:
        return ui.nav_panel("Cluster", ui.markdown("_No cluster modules found._"))

    choices = {mid: mod.LABEL for mid, mod in cluster_modules.items()}

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


def visualization_panel(visualization_modules: dict) -> ui.Tag:
    if not visualization_modules:
        return ui.nav_panel(
            "Visualization", ui.markdown("_No visualization modules found._")
        )

    choices = {mid: mod.LABEL for mid, mod in visualization_modules.items()}

    accordion_panels = []
    for module_id, mod in visualization_modules.items():
        description = getattr(mod, "DESCRIPTION", None)
        accordion_panels.append(
            ui.accordion_panel(
                mod.LABEL,
                _description_accordion(module_id, description)
                if description
                else ui.tags.span(),
                *[param_to_ui(module_id, p) for p in mod.PARAMS],
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
        ),
    )


def _help_panel() -> ui.Tag:
    readme_path = Path(__file__).parent.parent / "README.md"
    try:
        readme_content = readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        readme_content = "_README.md not found._"
    except Exception as e:
        readme_content = f"_Error loading README.md: {e}_"

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
) -> ui.Tag:
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
        open="always",
        fillable=True,
        border=True,
        border_radius=True,
        border_color="#000000",
        padding=15,
        bg="#eeeeee",
    )
