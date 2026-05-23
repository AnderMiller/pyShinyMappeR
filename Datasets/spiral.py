from typing import Any

import numpy as np

from Helpers.param import NumericParam, SliderParam
from Helpers.results import DatasetResult

LABEL = "Spiral"

DESCRIPTION = """
### Spiral

Each arm is a parametric curve where a point at parameter $t \\in [0, 1]$
is placed at angle $\\theta(t)$ and radius $r(t)$:

$$
\\theta(t) = 2\\pi \\cdot n_{\\text{turns}} \\cdot t +
\\frac{2\\pi \\cdot k}{n_{\\text{arms}}}
$$

$$
r(t) = r_{\\text{start}} + (r_{\\text{end}} - r_{\\text{start}}) \\cdot t^{\\alpha}
$$

giving Cartesian coordinates

$$
(x, y) = r(t)\\cdot(\\cos\\theta(t), \\sin\\theta(t))
+ \\lambda \\cdot \\text{Noise}(\\sigma)
$$

where $k$ is the arm index and $\\alpha$ is the **radius exponent**.

---

The **radius exponent** $\\alpha$ controls the spacing of points along each arm:

- *$\\alpha = 1$:*  Archimedean — uniform radial spacing.
- *$\\alpha < 1$:*  Points compressed toward the outside.
- *$\\alpha > 1$:*  Points compressed toward the center (Fermat-like).

---

**Noise** controls the distribution of the additive noise (e.g.,
the function $\\text{Noise}(\\sigma)$):

- *Gaussian:*  $\\mathcal{N}(0, \\sigma^2)$ applied independently in $x$ and $y$.
"""

PARAMS = [
    SliderParam(
        id="n_points",
        label="Number of Points $ ( N ) $",
        min=10,
        max=2000,
        value=300,
        step=10,
    ),
    SliderParam(
        id="n_turns",
        label="Number of Turns $ ( n_{\\text{turns}} ) $",
        min=1,
        max=10,
        value=3,
        step=1,
    ),
    SliderParam(
        id="n_arms",
        label="Number of Arms $ ( n_{\\text{arms}} ) $",
        min=1,
        max=6,
        value=1,
        step=1,
    ),
    SliderParam(
        id="start_radius",
        label="Start Radius $ ( r_{\\text{start}} ) $",
        min=0.0,
        max=2.0,
        value=0.0,
        step=0.1,
    ),
    SliderParam(
        id="end_radius",
        label="End Radius $ ( r_{\\text{end}} ) $",
        min=0.5,
        max=5.0,
        value=2.0,
        step=0.1,
    ),
    SliderParam(
        id="exponent",
        label="Radius Exponent $ ( \\alpha ) $",
        min=0.5,
        max=3.0,
        value=1.0,
        step=0.1,
    ),
    SliderParam(
        id="noise_weight",
        label="Noise Weight $ ( \\lambda ) $",
        min=0.0,
        max=1.0,
        value=0.05,
        step=0.01,
    ),
    SliderParam(
        id="noise_scale",
        label="$ \\text{Noise Scale } ( \\sigma ) $",
        min=0.0,
        max=0.5,
        value=0.05,
        step=0.01,
    ),
    NumericParam(
        id="seed",
        label="Random Seed",
        value=42,
        min=0,
        max=99999,
        step=1,
    ),
]


def generate(params: dict) -> np.ndarray:
    rng = np.random.default_rng(int(params["seed"]))

    n_points = params["n_points"]
    n_arms = params["n_arms"]
    points_per_arm = n_points // n_arms
    remainder = n_points % n_arms

    arms = []
    for arm_idx in range(n_arms):
        n = points_per_arm + (1 if arm_idx < remainder else 0)
        t = np.linspace(0, 1, n)

        arm_offset = (2 * np.pi * arm_idx) / n_arms
        angle = t * params["n_turns"] * 2 * np.pi + arm_offset

        radius = (
            params["start_radius"]
            + (params["end_radius"] - params["start_radius"]) * t ** params["exponent"]
        )

        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        noise = rng.normal(0, params["noise_scale"], (n, 2))
        arms.append(np.column_stack([x, y]) + params["noise_weight"] * noise)

    return np.vstack(arms)


def result(params: dict, modules: Any = None, module_id: Any = None):
    return DatasetResult(
        params=params,
        module_id=module_id,
        modules=modules,
        label=LABEL,
        data=generate(params),
    )
