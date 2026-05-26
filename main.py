from pathlib import Path

from shiny import App, ui
from shinywidgets import output_widget

from Helpers.loader import load_modules
from Helpers.server import make_server
from Helpers.ui_builder import build_sidebar

DATASETS_DIR = Path(__file__).parent / "Datasets"
FILTERS_DIR = Path(__file__).parent / "Lenses"
COVER_DIR = Path(__file__).parent / "Coverers"
CLUSTER_DIR = Path(__file__).parent / "Clusterers"
VISUALIZATION_DIR = Path(__file__).parent / "Visualizations"

DATASET_MODULES = load_modules(
    directory=DATASETS_DIR,
    required_attrs=("LABEL", "PARAMS", "generate"),
    namespace_prefix="datasets",
)

FILTER_MODULES = load_modules(
    directory=FILTERS_DIR,
    required_attrs=("LABEL", "PARAMS", "OUTPUT_DIM", "filter"),
    namespace_prefix="lenses",
)

COVER_MODULES = load_modules(
    directory=COVER_DIR,
    required_attrs=("LABEL", "PARAMS", "cover"),
    namespace_prefix="coverers",
)

CLUSTER_MODULES = load_modules(
    directory=CLUSTER_DIR,
    required_attrs=("LABEL", "PARAMS", "cluster"),
    namespace_prefix="clusterers",
)

VISUALIZATION_MODULES = load_modules(
    directory=VISUALIZATION_DIR,
    required_attrs=("LABEL", "PARAMS"),
    namespace_prefix="visualizations",
)


MATHJAX_CONFIG = ui.tags.script(
    """
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$']],
            displayMath: [['$$', '$$']],
            processEscapes: true,
        },
        options: {
            skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
        },
    };
    """,
    type="text/javascript",
)

MATHJAX_SCRIPT = ui.tags.script(
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js",
    type="text/javascript",
    id="MathJax-script",
    async_="true",
)

app_ui = ui.page_fillable(
    ui.head_content(MATHJAX_CONFIG, MATHJAX_SCRIPT),
    ui.layout_sidebar(
        build_sidebar(
            DATASET_MODULES,
            FILTER_MODULES,
            COVER_MODULES,
            CLUSTER_MODULES,
            VISUALIZATION_MODULES,
        ),
        ui.div(
            *[
                panel
                for mod_id, mod in VISUALIZATION_MODULES.items()
                for panel in (
                    ()
                    if not hasattr(mod, "render_matplotlib")
                    else ui.panel_conditional(
                        f"input.visualization_select.includes('{mod_id}')",
                        ui.card(
                            ui.card_body(
                                ui.output_plot(
                                    f"matplotlib__{mod_id}",
                                ),
                                padding=0,
                            ),
                        ),
                    ),
                    ()
                    if not hasattr(mod, "render_plotly")
                    # Plotly card — only if module has render_plotly
                    else ui.panel_conditional(
                        f"input.visualization_select.includes('{mod_id}')",
                        ui.card(
                            ui.card_body(
                                output_widget(
                                    f"plotly__{mod_id}",
                                ),
                                padding=0,
                            ),
                        ),
                    ),
                )
            ],
            id="viz_container",
        ),
    ),
)

app = App(
    app_ui,
    make_server(
        DATASET_MODULES,
        FILTER_MODULES,
        COVER_MODULES,
        CLUSTER_MODULES,
        VISUALIZATION_MODULES,
    ),
    debug=False,
)
