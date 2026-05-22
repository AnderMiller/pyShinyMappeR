# List inputs
default:
    @just --list

# Build the paper
build:
    cd paper && latexmk

# Rebuild paper when .tex or bib files change
write:
    @echo "Watching paper/ for changes..."
    watchexec \
        --exts tex,bib,sty,cls \
        --watch paper \
        --restart \
        --clear \
        -- just build


alias fmt := format
# Format all the code
format:
    nix fmt flake.nix
    ruff format .
    ruff check --fix .


# Lint R code
lint:
    ruff format --check .
    ruff check


# Start shinymapper app
app:
  shiny run main.py

# Test the code
test:
    echo "Will use pytest. Tests not yet implemented."
