# pyShinyMappeR

An interactive Shiny application for visualizing the effect of varying
hyperparameters in the Mapper algorithm. Built with
[Shiny for Python](https://shiny.posit.co/py/).

---

The Mapper algorithm is a staple in Topological Data Analysis (TDA). This 
shiny-app is an educational and research tool which makes comparing results 
between different mapper parameters simple. The app was written on top of 
Zen Mapper and is modular in order to be extensible by future researchers who
want to implement and compare various methods. The app was also enables 
built-in interactive documentation for each aspect of the mapper algorithm.


---

## Project structure

There is a directory for each aspect of the Mapper Algorithm and the state of the 
application. Files in these directories (excluding `/Helpers/`) which satisfy
requirements will be auto-loaded into the app ui. The `Helpers` directory 
includes code which are used to facilitate app functionality. For example: the 
`ui_builder.py` helper parses a `PARAMS` constant inside of each auto-loaded 
module file and populates the left side-bar with appropriate interactive widgets.

`main.py` is the entry point into the shiny app: loading modules and initiating 
the server. While `Helpers/server.py` contains logic for the reactives in the
shinyapp.

`Helpers/results.py` and `Helpers/param.py` contain the dataclasses used and 
expected by the server. Parameter types are effectively wrapped versions for 
kwargs in their corresponding ui elements in shiny. The Param types are called in 
`ui_builder.py` and `ui_controller.py` and are expected elements in each module's
`PARAMS` list. `ui_controller.py` can be thought of as tools for updating the 
`PARAMS` state while the app is running. Each module except for visualizations
are expected to return a `___Result` object. This makes passing new metadata 
elements for a result as easy as adding an optional attribute to the 
corresponding `_Result` object inside of `results.py`. This was chosen so as 
to be easy to develop on top of without leading to breaking changes inside of 
other modules.

Lastly, and most likely where people will first look to modify things, is the 
Visualization Modules. This is the only section which, while populated 
automatically by the loader does not return a VisualizationResult object. 
Instead each visualization module must have a `render_matplotlib` and/or a 
`render_plotly` function. These are then rendered by `server.py` when selected by 
the user in the UI. These functions should return a corresponding matplotlib or 
plotly Figure object. Future work may change render_plotly into a render_widget 
function in order to leverage the ShinyWidgets package extensions. However, 
as of now the support for ShinyWidgets does not appear to be a priority and 
plotly's functionality appears to suffice.



---

## Module APIs

Modules in the `Datasets`, `Lenses`, `Coverers`, `Clusterers`, and `Visualizations`
directories are **auto-discovered** by `Helpers/loader.load_modules()` at 
the start of the app. Adding a `*.py` file which does not start with `_` and
contains the corresponding required attributes for each Module type is 
sufficient to make it appear as an option in the App. Each of the 
non-Visualization modules are expected to have a `result()` function. This
result function must return a corresponding `_Result` object as in 
`Helpers/results.py`.

In general, each module file must have a `LABEL` variable which is a string
used to fill in UI elements referring to that module. Additionally each module 
may include a `DESCRIPTION` variable. `DESCRIPTION` is a string which (like `LABEL`) 
may include LaTeX code formated with `$` or `$$`. This is used to 
populate an accordion tab in the app UI which is rendered via MathJax.

`_Result` objects have attributes `module_id` and `module` which are set by the 
filename and location of the module and are passed in as keyword arguments to 
the given modules `result()` function when called by the server. The `LABEL` and
`PARAMS` constants of the module is used to automatically create the .label and
.params attributes and keyword arguments passed into the `results()` function in
the server. Doing it this way allows for a single module file to control the vast
majority of its part of the app's function. For example `server.py` logic for getting the parameter looks like:

```python
# in Helpers/server.py...
params = {p.id: input[f"{module_id}__{p.id}"]() for p in mod.PARAMS}
```
While setting initial params and modifying params using app state can be done 
inside of the single module file by setting a `PARAMS` constant and defining 
an `update_ui` function like so:

```python
# Taken from Visualizations/cover_element_view.py

LABEL = "Cover Element Explorer"
PARAMS = [
    # ..., Other Parameter objects
    SliderParam(
        id="selected_cover_element",
        label="Cover Element",
        min=1,
        max=10,
        value=1,
        step=1,
    ),
    #...
]


def update_ui(ctx: Context, mapper_result: MapperResult, mod_id: str):
    n_elements = len(mapper_result.cover)
    # ID as in param_to_ui
    slider_id = f"{mod_id}__selected_cover_element"

    if ctx.ui is not None:
        current_val = ctx.ui.input[slider_id]()

        ctx.ui.update_slider(
            slider_id=slider_id,
            param=SliderParam(
                id="selected_cover_element",
                label="Cover Element",
                value=min(n_elements, current_val),
                min=1,
                max=n_elements,
                step=1,
            ),
        )

```

This isolates the actual setting of parameters, checking state, or modifying 
the shiny server logic to be inside individual module files.

Note that `results.py` contains the definition of the `Context` object which 
contains the server information which could be used inside of any `update_ui()` function.

---

## Writing descriptions

The optional `DESCRIPTION` and `LABEL` strings each support Markdown and LaTeX (rendered via MathJax 3). Use `$...$` for inline math and `$$...$$` for 
display math. Use `\\` for LaTeX backslashes inside Python strings.

#### Example:

```python
DESCRIPTION = """
### My Dataset

Points are sampled from the unit circle:

$$
(x, y) = (\\cos\\theta, \\sin\\theta) + \\mathcal{N}(0, \\sigma^2)
$$

where $\\sigma$ is the **noise** level.
"""
```

## Running the app

Easiest way is having Nix installed:

```bash
nix develop
uv venv .venv
source .venv/bin/activate
uv sync
just app
```
