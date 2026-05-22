import numpy as np

from Helpers.param import Param

LABEL = "Circle"

DESCRIPTION = """
The circle is the simplest dataset with non-trivial topology. It should be used as the first 
sanity-check example when implementing any sort of TDA methodology. 

This dataset samples angles from the domain $[0, \\theta_{\\max}] \\subseteq [0, 2 \\pi ]$ and 
passes them to the unit circle by the standard parameterization. Various noise distributions with weight $\\lambda$ can be added to each point 
in $\\mathbb{R}^{2}$. So our dataset is made up of points in the form:

$$
(x, y) = (\\cos\\theta, \\sin\\theta) + \\lambda \cdot \\text{Noise}(\\sigma)
$$

---


The **Theta sampling** parameter controls how $\\theta$ is drawn from $[0, \\theta_{\\max}]$:

- *Uniform:*  $\\theta \\sim \\text{Uniform}(0, \\theta_{\\max})$.

- *Normal:*  $\\theta \\sim \\mathcal{N}(\\theta_{\\max}/2, (\\theta_{\\max}/4)^2)$.

- *Fibonacci:*  Maximally spread (Deterministic).

---

**Noise type** controls the distribution of the additive noise (e.g., the function $ \\text{Noise}(\\sigma)$):

- *Gaussian:*  $ \\mathcal{N}(0, \\sigma^2)$
- *Uniform:*  $\\text{Uniform}(-\\sigma, \\sigma)$
- *Radial:*  $\\mathcal{N}(0, \\sigma^2)$ noise is applied radially
"""

PARAMS = [
    Param(
        id="n_points",
        type="slider",
        label="Number of Points $ ( N ) $ ",
        min=10,
        max=1000,
        value=200,
        step=10,
    ),
    Param(
        id="theta_range",
        type="slider",
        label="Theta Range $( \\theta_{\\text{max}} ) $ ",
        min=0.0,
        max=round(2 * np.pi, 4),
        value=round(2 * np.pi, 4),
        step=0.01,
    ),
    Param(
        id="theta_sampling",
        type="select",
        label="$ \\theta \\text{-Sampling} $",
        choices=("uniform", "normal", "fibonacci"),
        value="uniform",
    ),
    Param(
        id="noise_weight",
        type="slider",
        label="Noise Weight $ ( \\lambda ) $ ",
        min=0.0,
        max=1.0,
        value=0.05,
        step=0.01,
    ),
    Param(
        id="noise_type",
        type="select",
        label="Noise Type",
        choices=("gaussian", "uniform", "radial"),
        value="gaussian",
    ),
    Param(
        id="noise_scale",
        type="slider",
        label=" $ \\text{Noise Scale }( \\sigma ) $ ",
        min=0.0,
        max=1.0,
        value=0.05,
        step=0.01,
    ),
    Param(
        id="seed",
        type="numeric",
        label="Random Seed",
        value=42,
        min=0,
        max=99999,
        step=1,
    ),
]


def _sample_theta(
    rng: np.random.Generator,
    n: int,
    theta_range: float,
    method: str,
) -> np.ndarray:
    match method:
        case "uniform":
            return rng.uniform(0, theta_range, n)
        case "normal":
            mu = theta_range / 2
            sigma = theta_range / 4
            if sigma <= 0:
                return np.zeros(n)
            result = rng.normal(mu, sigma, n)
            oob = (result < 0) | (result > theta_range)
            while oob.any():
                result[oob] = rng.normal(mu, sigma, oob.sum())
                oob = (result < 0) | (result > theta_range)
            return result
        case "fibonacci":
            golden = (1 + np.sqrt(5)) / 2
            return (np.arange(n) / golden % 1) * theta_range
        case _:
            raise ValueError(f"Unknown theta sampling method: '{method}'")


def _sample_noise(
    rng: np.random.Generator,
    n: int,
    sigma: float,
    theta: np.ndarray,
    method: str,
) -> np.ndarray:
    match method:
        case "gaussian":
            return rng.normal(0, sigma, (n, 2))
        case "uniform":
            return rng.uniform(-sigma, sigma, (n, 2))
        case "radial":
            magnitude = rng.normal(0, sigma, n)
            radial_dir = np.column_stack([np.cos(theta), np.sin(theta)])
            return (radial_dir.T * magnitude).T
        case _:
            raise ValueError(f"Unknown noise type: '{method}'")


def generate(params: dict) -> np.ndarray:
    rng = np.random.default_rng(int(params["seed"]))

    n = params["n_points"]
    theta = _sample_theta(rng, n, params["theta_range"], params["theta_sampling"])
    noise = _sample_noise(rng, n, params["noise_scale"], theta, params["noise_type"])

    return (
        np.column_stack([np.cos(theta), np.sin(theta)]) + params["noise_weight"] * noise
    )
