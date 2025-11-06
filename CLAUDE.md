# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python library for declarative floorplan generation and manipulation. The project uses uv for fast dependency management and follows the src-layout package structure.

## Development Commands

### Formatting 

Use Ruff for formatting

### Environment Setup
```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>
```

### Running Code
```bash
# Run Python with the project environment
uv run python -c "from declarative_floorplan import hello; print(hello())"

# Run a script
uv run python your_script.py

# Start interactive Python shell
uv run python
```

### Building and Publishing
```bash
# Build the package
uv build

# The built distributions will be in the dist/ directory
```

### Testing
```bash
# Install pytest (if not already added)
uv add --dev pytest

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=declarative_floorplan
```


## Project Structure

- **src/declarative_floorplan/**: Main package directory (src-layout)
  - `__init__.py`: Package initialization
  - `py.typed`: Marker for PEP 561 type hint support
- **pyproject.toml**: Project metadata and dependencies (managed by uv)
- **.python-version**: Python version specification (3.12)

## Architecture

*To be documented as the architecture evolves*
