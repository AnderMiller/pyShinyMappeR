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

We separate implementation files into the following directories.

## Datasets:
Supply a list of options for the dataset generation.

Return:
    2D numpy arrays or R/pandas dataframes.

## Cover Schemes
Supply a list of options/variables for the cover scheme for the side panel.
A flag for the lens function output dimension so that appropriate cover schemes can be used.

Returns:
    (list(list(ids)), metadata)
        Where each interior list of the first tuple entry is a cover element. The second element 
        of the tuple should contain visualization information needed for helpers.
        E.g., metadata=("global_view", "draw_rectangles", other parameters])

## Lens Functions
A flag for the dimension of the output so that the lens function or cover scheme is not shown
when cover schemes are incompatible.

## Clustering Algorithms

## Helpers
This is where we put in visualization/helper code for the App

