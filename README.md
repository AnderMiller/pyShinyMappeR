my .envrc is:

```bash
    use flake
    uv venv .venv --no
    source .venv/bin/activate
```

# Thesis:

pyShinyMapper is a shiny app for visualizing the effect of varying the Hyper-parameters 
in the mapper algorithm. Since most mapper implementations are written in either Python 
or R the architecture is built for an atomic approach using either R or Python files.
The core shiny logic is written in Python.

We should also be able to change the backend computation to use either mappeR or Zen Mapper 
after being given all information needed to compute the mapper graph.

We separate out visualization and implementation processes as follows.

## Datasets:
We restrict to 2D.

## Cover Schemes

## Lens Functions

## Clustering Algorithms

## Helpers
This is where we put in visualization/helper code for the App

