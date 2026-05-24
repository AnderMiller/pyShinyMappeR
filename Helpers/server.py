import zen_mapper as zm
from shiny import Inputs, Outputs, Session, reactive, render
from zen_mapper.types import MapperResult

from Helpers.results import (
    ClustererResult,
    Context,
    CovererResult,
    DatasetResult,
    FilterResult,
)
from Helpers.ui_controller import UIController


def make_server(
    dataset_modules: dict,
    filter_modules: dict,
    cover_modules: dict,
    cluster_modules: dict,
    visualization_modules: dict,
):

    def server(input: Inputs, output: Outputs, session: Session):

        @reactive.calc
        def current_dataset() -> DatasetResult:
            module_id = input.dataset_select()
            mod = dataset_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            return mod.result(
                params=params, modules=dataset_modules, module_id=module_id
            )

        @reactive.calc
        def current_filtered_dataset() -> FilterResult:
            dataset = current_dataset()
            module_id = input.filter_select()
            mod = filter_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            return mod.result(
                dataset=dataset,
                params=params,
                modules=filter_modules,
                module_id=module_id,
            )

        @reactive.calc
        def current_cover() -> CovererResult:
            module_id = input.cover_select()
            mod = cover_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            return mod.result(
                data=current_dataset(),
                filtered=current_filtered_dataset(),
                params=params,
                modules=cover_modules,
                module_id=module_id,
            )

        @reactive.calc
        def current_cluster() -> ClustererResult:
            module_id = input.cluster_select()
            mod = cluster_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            return mod.result(
                data=current_dataset(),
                filtered=current_filtered_dataset(),
                cover=current_cover(),
                params=params,
                modules=cover_modules,
                module_id=module_id,
            )

        @reactive.calc
        def current_mapper_result() -> MapperResult:
            return zm.mapper(
                data=current_dataset().data,
                projection=current_filtered_dataset().filtered_data,
                cover_scheme=current_cover().cover,
                clusterer=current_cluster().clusterer,
                dim=1,  # TODO: Maybe don't hardcode 1D Mapper!
            )

        @reactive.calc
        def current_context() -> Context:
            print(input["cover_element_view__selected_cover_element"]())

            return Context(
                dataset=current_dataset(),
                filter=current_filtered_dataset(),
                coverer=current_cover(),
                clusterer=current_cluster(),
                ui=UIController(
                    session=session,
                    input=input,
                ),
            )

        @reactive.effect
        def _auto_update_ui():
            for mod_id, mod in visualization_modules.items():
                if hasattr(mod, "update_ui"):
                    mod.update_ui(
                        ctx=current_context(),
                        mapper_result=current_mapper_result(),
                        mod_id=mod_id,
                    )

        def draw_plots(mod_id: str, mod):
            """
            Closes over mod_id and mod so each renderer is independent.
            Returns None (empty plot) when the module is not checked.
            """

            @output(id=f"visualizations__{mod_id}")
            @render.plot
            def _plot_renderer():
                if mod_id not in (input.visualization_select() or []):
                    return None

                ctx = current_context()
                mapper_result = current_mapper_result()
                params = {p.id: input[f"{mod_id}__{p.id}"]() for p in mod.PARAMS}
                if mod.render:
                    return mod.render(
                        ctx=ctx, mapper_result=mapper_result, params=params
                    )
                raise ValueError(f"{mod_id} does not have a render function.")
                # TODO: if other draw functions are implemented this should
                # fail gracefully

        for vid, vmod in visualization_modules.items():
            draw_plots(vid, vmod)

    return server
