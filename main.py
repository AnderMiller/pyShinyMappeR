from pathlib import Path

from shiny import App, ui

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
    required_attrs=("LABEL", "PARAMS", "render"),
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
        # ui.output_plot("main_plot"),
        # reserve a spot for plots
        ui.div(
            *[
                ui.panel_conditional(
                    f"input.visualization_select.includes('{mod_id}')",
                    ui.output_plot(f"visualizations__{mod_id}"),
                )
                for mod_id in VISUALIZATION_MODULES
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
)
