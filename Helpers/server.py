from logging import getLogger

import zen_mapper as zm
from shiny import Inputs, Outputs, Session, reactive, render
from shinywidgets import render_plotly
from zen_mapper.types import MapperResult

from Helpers.results import (
    ClustererResult,
    Context,
    CovererResult,
    DatasetResult,
    FilterResult,
)
from Helpers.ui_controller import UIController

logger = getLogger(__name__)


def make_server(
    dataset_modules: dict,
    filter_modules: dict,
    cover_modules: dict,
    cluster_modules: dict,
    visualization_modules: dict,
):
    def _merge_dict(*dict_args):
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    # for convenience
    all_modules = _merge_dict(
        dataset_modules,
        filter_modules,
        cover_modules,
        cluster_modules,
        visualization_modules,
    )

    def server(input: Inputs, output: Outputs, session: Session):

        @reactive.calc
        def current_dataset() -> DatasetResult:
            module_id = input.dataset_select()
            mod = dataset_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}

            logger.info(f"UPDATING DATASET: \n {module_id}: {params}")
            return mod.result(
                params=params, modules=dataset_modules, module_id=module_id
            )

        @reactive.calc
        def current_filtered_dataset() -> FilterResult:
            dataset = current_dataset()
            module_id = input.filter_select()
            mod = filter_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            logger.info(f"UPDATING FILTER: \n {module_id}: {params}")
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
            logger.info(f"UPDATING COVER: \n {module_id}: {params}")
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
            logger.info(f"UPDATING CLUSTERER: \n {module_id}: {params}")
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
            logger.info("UPDATING MAPPER RESULT...")
            return zm.mapper(
                data=current_dataset().data,
                projection=current_filtered_dataset().filtered_data,
                cover_scheme=current_cover().cover,
                clusterer=current_cluster().clusterer,
                dim=1,  # TODO: Maybe don't hardcode 1D Mapper!
            )

        @reactive.calc
        def current_context() -> Context:
            logger.info("UPDATING CONTEXT...")
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
            for mod_id, mod in all_modules.items():
                if hasattr(mod, "update_ui"):
                    logger.info(f"AUTO UPDATING UI FOR {mod_id}...")
                    mod.update_ui(
                        ctx=current_context(),
                        mapper_result=current_mapper_result(),
                        mod_id=mod_id,
                    )

        def draw(mod_id: str, mod):
            """
            Closes over mod_id and mod so each renderer is independent.
            Returns None (empty plot) when the module is not checked.
            """

            @output(id=f"matplotlib__{mod_id}")
            @render.plot
            def _matplotlib_renderer():
                if mod_id not in (input.visualization_select() or []):
                    logger.info(f"{mod_id} is not selected, returning None")
                    return None

                # if no render_matplotlib return None
                if not hasattr(visualization_modules[mod_id], "render_matplotlib"):
                    logger.info(
                        f"{mod_id}: render_matplotlib function does \
                                    not exist, returning None"
                    )
                    return None

                ctx = current_context()
                mapper_result = current_mapper_result()
                params = {p.id: input[f"{mod_id}__{p.id}"]() for p in mod.PARAMS}
                if mod.render_matplotlib:
                    logger.info(f"{mod_id}: RENDERING matplotlib plot.")
                    return mod.render_matplotlib(
                        ctx=ctx,
                        mapper_result=mapper_result,
                        params=params,
                    )

            @output(id=f"plotly__{mod_id}")
            @render_plotly
            def _plotly_renderer():
                if mod_id not in (input.visualization_select() or []):
                    logger.info(f"{mod_id} is not selected, returning None")
                    return None
                # if no render_plotly return None
                if not hasattr(visualization_modules[mod_id], "render_plotly"):
                    logger.info(
                        f"{mod_id}: render_plotly function does \
                                    not exist, returning None"
                    )
                    return None

                ctx = current_context()
                mapper_result = current_mapper_result()
                params = {p.id: input[f"{mod_id}__{p.id}"]() for p in mod.PARAMS}

                if mod.render_plotly:
                    logger.info(f"{mod_id}: RENDERING plotly.")
                    return mod.render_plotly(
                        ctx=ctx,
                        mapper_result=mapper_result,
                        params=params,
                    )

        for vid, vmod in visualization_modules.items():
            draw(vid, vmod)

    return server
