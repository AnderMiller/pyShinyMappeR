# pyShinyMappeR

A interactive Shiny application for visualizing the effect of varying
hyperparameters in the Mapper algorithm. Built with
[Shiny for Python](https://shiny.posit.co/py/).

In general: the result object is defined in Helpers/results.py
The result object for each aspect is updated/populated inside of server.py

---

## Running the app

Easiest way is having Nix installed:

```bash
nix develop
just app
```

---

## Project structure

Each of the five module directories is **auto-discovered** at startup.
Adding a new `.py` file to any of them is sufficient to make it appear
in the app.

---

## Module APIs

TODO

---

### `Datasets/`

Generates the raw point cloud passed to the rest of the pipeline.

---

...

---

### `Visualizations/`

...

---

## Defining parameters

...

---

## Writing descriptions

The optional `DESCRIPTION` string supports Markdown and LaTeX (rendered
via MathJax 3). Use `\$...\$` for inline math and `\$\$...\$\$` for display
math. Use `\\\\` for LaTeX backslashes inside Python strings.

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
