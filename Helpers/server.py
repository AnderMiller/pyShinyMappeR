import zen_mapper as zm
from shiny import Inputs, Outputs, Session, reactive, render, ui
from zen_mapper.types import MapperResult

from Helpers.results import ClustererResult, CovererResult, DatasetResult, FilterResult


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
            return DatasetResult(
                data=mod.generate(params),
                params=params,
                module_id=module_id,
                modules=dataset_modules,
                label=mod.LABEL,
            )

        @reactive.calc
        def current_filtered_dataset() -> FilterResult:
            data = current_dataset().data
            module_id = input.filter_select()
            mod = filter_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            return FilterResult(
                filtered_data=mod.filter(data=data, params=params),
                params=params,
                module_id=module_id,
                modules=filter_modules,
                label=mod.LABEL,
                # define function for trying module arguments.
                # this sort of takes care of "supported blank"
                # Should also update result classes.
                line=None,
            )

        @reactive.calc
        def current_cover() -> CovererResult:
            module_id = input.cover_select()
            mod = cover_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            return CovererResult(
                cover=mod.cover(params),
                params=params,
                module_id=module_id,
                label=mod.LABEL,
                modules=cover_modules,
            )

        @reactive.effect
        def _update_selected_cover_element_sliders():
            # if you need a slider that selects based on cover element
            n_covers = len(current_mapper_result().cover)

            for vid, vmod in visualization_modules.items():
                if any(p.id == "selected_cover_element" for p in vmod.PARAMS):
                    slider_id = f"{vid}__selected_cover_element"
                    current_val = input[slider_id]()
                    ui.update_slider(
                        id=slider_id,
                        max=n_covers,
                        value=min(current_val, n_covers),
                        session=session,
                    )

        @reactive.calc
        def current_cluster() -> ClustererResult:
            module_id = input.cluster_select()
            mod = cluster_modules[module_id]
            params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
            return ClustererResult(
                clusterer=mod.cluster(params),
                params=params,
                module_id=module_id,
                modules=cluster_modules,
                label=mod.LABEL,
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

        def make_renderer(mod_id: str, mod):
            """
            Closes over mod_id and mod so each renderer is independent.
            Returns None (empty plot) when the module is not checked.
            """

            @output(id=f"visualizations__{mod_id}")
            @render.plot
            def _renderer():
                if mod_id not in (input.visualization_select() or []):
                    return None

                data = current_dataset()
                filtered = current_filtered_dataset()
                cover = current_cover()
                result = current_mapper_result()
                params = {p.id: input[f"{mod_id}__{p.id}"]() for p in mod.PARAMS}
                return mod.render(data, filtered, cover, result, params)

        for vid, vmod in visualization_modules.items():
            make_renderer(vid, vmod)

        # @render.plot
        # def main_plot():
        #     data = current_dataset()
        #     result = current_mapper_result()
        #     fig, ax = plt.subplots()
        #     if data.shape[1] >= 2:
        #         ax.scatter(data[:, 0], data[:, 1], s=10, alpha=0.6)
        #         nx.draw(zm.to_networkx(result.nerve))
        #     ax.set_title(dataset_modules[input.dataset_select()].LABEL)
        #     return fig

    return server
