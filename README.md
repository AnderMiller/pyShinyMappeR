# pyShinyMappeR

A interactive Shiny application for visualizing the effect of varying
hyperparameters in the Mapper algorithm. Built with
[Shiny for Python](https://shiny.posit.co/py/).

In general: the result object is defined in Helpers/results.py
The result object for each aspect is updated/populated inside of server.py

---

## Running the app

```bash
shiny run main.py --reload
```

---

## Project structure

```text
pyShinyMappeR/
├── main.py                  ← App entry point
│
├── Datasets/                ← Data generation modules
├── Filters/                 ← Lens/filter function modules
├── Covers/                  ← Cover scheme modules
├── Clusterers/              ← Clustering algorithm modules
├── Visualizations/          ← Plot/render modules
│
└── Helpers/                 ← Internal app infrastructure
    ├── __init__.py
    ├── loader.py            ← Auto-discovery via importlib
    ├── param.py             ← Frozen Param dataclass
    ├── ui_builder.py        ← Param → Shiny UI, sidebar assembly
    └── server.py            ← Reactive pipeline
```

Each of the five module directories is **auto-discovered** at startup.
Adding a new `.py` file to any of them is sufficient to make it appear
in the app — no changes to `main.py` or `Helpers/` are needed.

---

## Mapper pipeline

Each tab in the sidebar corresponds to one stage of the Mapper pipeline.
Data flows top-to-bottom; each stage depends only on the output of the
stage before it.

```text
Datasets/                Filters/                  Covers/
generate(params)    →    filter(data, params)  →   cover(filtered, params)
    │                         │                         │
    ▼                         ▼                         ▼
np.ndarray              np.ndarray               list[list[int]]
(N, d)                  (N, 1) or (N, 2)         cover elements
                        same N                   (indices into data)
                                                      │
                                          ┌───────────┘
                                          ▼
                                    Clusterers/
                              cluster(data, cover, params)
                                          │
                                          ▼
                                   list[list[int]]
                                   mapper nodes
                                   (indices into data)
                                          │
                              ┌───────────┘
                              ▼
                        Visualizations/
                render(data, filtered, cover, nodes, params)
                              │
                              ▼
                        Figure (matplotlib)
```

---

## Module APIs

All modules share three **optional** conventions:

| Attribute | Type | Description |
|---|---|---|
| `LABEL` | `str` | ✅ Required. Display name in the sidebar selector. |
| `PARAMS` | `list[Param]` | ✅ Required. Controls rendered in the sidebar. |
| `DESCRIPTION` | `str` | Optional. Markdown + LaTeX string shown in a collapsible accordion. |

The `Param` dataclass is defined in `Helpers/param.py` — see
[Defining parameters](#defining-parameters) below.

---

### `Datasets/`

Generates the raw point cloud passed to the rest of the pipeline.

```python
LABEL: str
PARAMS: list[Param]
DESCRIPTION: str          # optional

def generate(params: dict) -> np.ndarray:
    """
    Returns an (N, d) array of N points in d dimensions.
    """
```

**Example:**

```python
# Datasets/circle.py
import numpy as np
from Helpers.param import Param

LABEL = "Circle"
PARAMS = [
    Param(id="n_points", type="slider", label="N", min=10, max=1000, value=200, step=10),
    Param(id="noise",    type="slider", label="Noise", min=0.0, max=0.5, value=0.05, step=0.01),
]

def generate(params: dict) -> np.ndarray:
    rng = np.random.default_rng()
    t = rng.uniform(0, 2 * np.pi, params["n_points"])
    noise = rng.normal(0, params["noise"], (params["n_points"], 2))
    return np.column_stack([np.cos(t), np.sin(t)]) + noise
```

---

### `Filters/`

Applies a lens function to the raw data, projecting it into 1D or 2D.
The output dimension is declared via `OUTPUT_DIM` so that incompatible
cover schemes can be hidden in the UI.

```python
LABEL: str
PARAMS: list[Param]
DESCRIPTION: str          # optional
OUTPUT_DIM: int           # 1 or 2

def filter(data: np.ndarray, params: dict) -> np.ndarray:
    """
    Receives:  (N, d) array
    Returns:   (N, 1) or (N, 2) array — same N, OUTPUT_DIM columns
    """
```

**Example:**

```python
# Filters/projection.py
import numpy as np
from Helpers.param import Param

LABEL = "Axis Projection"
OUTPUT_DIM = 1
PARAMS = [
    Param(id="axis", type="select", label="Axis", choices=("x", "y"), value="x"),
]

def filter(data: np.ndarray, params: dict) -> np.ndarray:
    col = 0 if params["axis"] == "x" else 1
    return data[:, col : col + 1]
```

---

### `Covers/`

Partitions the filtered values into overlapping cover elements.
`ACCEPTS_DIM` declares which filter output dimensions this cover scheme
supports; incompatible covers will be hidden when an incompatible filter
is selected.

```python
LABEL: str
PARAMS: list[Param]
DESCRIPTION: str                        # optional
ACCEPTS_DIM: int | tuple[int, ...]      # e.g. 1, 2, or (1, 2)

def cover(filtered: np.ndarray, params: dict) -> list[list[int]]:
    """
    Receives:  (N, 1) or (N, 2) array of filtered values
    Returns:   list of cover elements, where each element is a list of
               integer indices into the original data array
    """
```

**Example:**

```python
# Covers/uniform_1d.py
import numpy as np
from Helpers.param import Param

LABEL = "Uniform 1D"
ACCEPTS_DIM = 1
PARAMS = [
    Param(id="n_intervals", type="slider", label="Intervals", min=2, max=50, value=10, step=1),
    Param(id="overlap",     type="slider", label="Overlap %", min=0.0, max=0.99, value=0.2, step=0.01),
]

def cover(filtered: np.ndarray, params: dict) -> list[list[int]]:
    vals = filtered[:, 0]
    lo, hi = vals.min(), vals.max()
    n = params["n_intervals"]
    step = (hi - lo) / n
    width = step * (1 + params["overlap"])
    elements = []
    for i in range(n):
        left  = lo + i * step - width / 2
        right = left + width
        elements.append(list(np.where((vals >= left) & (vals <= right))[0]))
    return [e for e in elements if e]
```

---

### `Clusterers/`

Clusters points within each cover element to form the nodes of the
Mapper graph.

```python
LABEL: str
PARAMS: list[Param]
DESCRIPTION: str          # optional

def cluster(
    data: np.ndarray,
    cover: list[list[int]],
    params: dict,
) -> list[list[int]]:
    """
    Receives:
        data   — original (N, d) point cloud
        cover  — list of cover elements (index lists)
        params — resolved parameter values

    Returns:
        list of nodes, where each node is a list of integer indices
        into the original data array. One cover element may produce
        multiple nodes.
    """
```

**Example:**

```python
# Clusterers/single_linkage.py
import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from Helpers.param import Param

LABEL = "Single Linkage"
PARAMS = [
    Param(id="threshold", type="slider", label="Distance Threshold",
          min=0.01, max=2.0, value=0.3, step=0.01),
]

def cluster(data: np.ndarray, cover: list[list[int]], params: dict) -> list[list[int]]:
    nodes = []
    for element in cover:
        if len(element) < 2:
            nodes.append(element)
            continue
        pts = data[element]
        Z = linkage(pts, method="single")
        labels = fcluster(Z, t=params["threshold"], criterion="distance")
        for cluster_id in np.unique(labels):
            nodes.append([element[i] for i, l in enumerate(labels) if l == cluster_id])
    return nodes
```

---

### `Visualizations/`

Renders the main plot. Receives all pipeline outputs so each module can
choose what to draw — a scatter plot might only use `data`, while a
Mapper graph visualization would use `nodes`.

```python
LABEL: str
PARAMS: list[Param]
DESCRIPTION: str          # optional

def render(
    data:     np.ndarray,       # original (N, d) point cloud
    filtered: np.ndarray,       # (N, 1) or (N, 2) lens values
    cover:    list[list[int]],  # cover elements
    nodes:    list[list[int]],  # clustered mapper nodes
    params:   dict,
) -> matplotlib.figure.Figure:
```

**Example:**

```python
# Visualizations/scatter.py
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from Helpers.param import Param

LABEL = "Scatter"
PARAMS = [
    Param(id="point_size", type="slider", label="Point Size", min=1, max=50, value=10, step=1),
    Param(id="alpha",      type="slider", label="Opacity", min=0.1, max=1.0, value=0.6, step=0.05),
]

def render(data, filtered, cover, nodes, params) -> Figure:
    fig, ax = plt.subplots()
    ax.scatter(data[:, 0], data[:, 1], s=params["point_size"], alpha=params["alpha"])
    ax.set_aspect("equal")
    return fig
```

---

## Defining parameters

Parameters are declared using the frozen `Param` dataclass from
`Helpers/param.py`. Because it is `frozen=True`, instances are immutable
and safe to share across modules.

```python
from Helpers.param import Param

Param(
    id:          str,                                        # unique within module
    type:        "slider" | "numeric" | "select" | "checkbox",
    label:       str,                                        # shown in sidebar
    value:       Any,                                        # default value
    min:         float | None = None,                        # slider / numeric
    max:         float | None = None,                        # slider / numeric
    step:        float | None = None,                        # slider / numeric
    choices:     tuple[str, ...] = (),                       # select only
)
```

---

## Writing descriptions

The optional `DESCRIPTION` string supports Markdown and LaTeX (rendered
via MathJax 3). Use `$...$` for inline math and `$$...$$` for display
math. Use `\\` for LaTeX backslashes inside Python strings.

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
