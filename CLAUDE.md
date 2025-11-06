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

```
src/declarative_floorplan/
├── __init__.py              # Public API exports
├── core/
│   ├── floorplan.py         # Floorplan context manager and coordinator
│   └── registry.py          # Element registration and tracking
├── geometry/
│   ├── vertex.py            # Vertex class with constraint support
│   └── constraints.py       # HorizontalConstraint, VerticalConstraint
├── elements/
│   ├── base.py              # Base class for all floorplan elements
│   ├── wall.py              # Wall element
│   ├── door.py              # Door element
│   ├── window.py            # Window element
│   └── opening.py           # Base class for Door/Window
├── positioning/
│   └── position.py          # Position enum (CENTERED, etc.)
└── rendering/
    ├── svg.py               # SVG generation engine
    ├── raster.py            # PNG/raster rendering (via CairoSVG)
    └── styles.py            # Style definitions (RenderConfig, ElementStyle)

examples/
├── simple_room/             # Basic room example
├── real_apartment/          # Complex apartment layout
└── gemeni_pro_2025_11_03/   # Generated floorplan example

mcp-servers/
└── visual-cot/              # MCP server for constraint visualization

render_examples.py           # Script to batch render all examples
```

## Architecture

### Core Design Principles
1. **Declarative API**: Users describe what they want, not how to build it
2. **Constraint-based positioning**: Vertices defined by HC/VC intersections
3. **Context manager pattern**: `with Floorplan() as fp:` for automatic registration
4. **Separation of concerns**: Elements handle geometry, renderers handle visualization

### Key Components

**Geometry Layer** (`geometry/`)
- Vertices defined by constraint intersections (HC + VC)
- HorizontalConstraint (HC): Defines a horizontal line at Y coordinate
- VerticalConstraint (VC): Defines a vertical line at X coordinate

**Elements Layer** (`elements/`)
- Wall: Linear element connecting two vertices
- Door/Window: Openings placed on walls with position and width
- Position can be numeric (distance from start) or semantic (Pos.CENTERED)

**Rendering Layer** (`rendering/`)
- SVGRenderer: Generates SVG markup from floorplan geometry
- RasterRenderer: Converts SVG to PNG/raster formats (uses CairoSVG and Pillow)
- RenderConfig: Customizable styling (colors, stroke widths, etc.)
- ElementStyle: Reusable style definitions

See RENDERING_GUIDE.md for detailed rendering documentation.

## Working with Examples

### Running Individual Examples
```bash
# Navigate to an example directory
cd examples/simple_room

# Run the model to generate output
uv run python model.py
```

### Batch Rendering All Examples
```bash
# Render all examples to PNG with optional overlays
uv run python render_examples.py

# Options (see script for details):
# - Renders each example's model.py to SVG and PNG
# - Can generate constraint overlays (constraints drawn on original image)
# - Can generate floorplan overlays (rendered plan on original image)
```

The `render_examples.py` script:
- Automatically finds all `model.py` files in `examples/`
- Imports the Floorplan object from each
- Generates SVG and PNG outputs
- Optionally creates visualization overlays using the MCP server tools

## MCP Server (Visual CoT)

The project includes an MCP server at `mcp-servers/visual-cot/` that provides tools for:

1. **draw_constraints**: Draw horizontal/vertical constraints from a model file overlaid on the original image
2. **overlay_floorplan**: Render a floorplan model and overlay it on the original image

These tools are useful for:
- Debugging constraint placement
- Comparing generated floorplans with source images
- Visual verification of model accuracy

The MCP server is automatically available when using Claude Code in this project.

## API Usage Example

```python
from declarative_floorplan import (
    Floorplan, Vertex, Wall, Door, Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC,
    RenderConfig, ElementStyle
)

# Create a simple room
with Floorplan("My Room") as fp:
    # Define constraints (reusable positioning lines)
    h_0, h_300 = HC(0), HC(300)
    v_0, v_400 = VC(0), VC(400)

    # Create vertices at constraint intersections
    bl = Vertex("Bottom Left", constraints=[h_0, v_0])
    br = Vertex("Bottom Right", constraints=[h_0, v_400])
    tl = Vertex("Top Left", constraints=[h_300, v_0])
    tr = Vertex("Top Right", constraints=[h_300, v_400])

    # Create walls connecting vertices
    bottom = Wall("Bottom", start_vertex=bl, end_vertex=br)
    right = Wall("Right", start_vertex=br, end_vertex=tr)
    top = Wall("Top", start_vertex=tr, end_vertex=tl)
    left = Wall("Left", start_vertex=tl, end_vertex=bl)

    # Add door and window
    Door("Entry", wall=bottom, position=Pos.CENTERED, width=30)
    Window("Window", wall=top, position=200, width=60)

    # Generate output
    fp.generate_svg("room.svg")  # SVG output
    fp.generate_png("room.png")  # PNG output (requires cairosvg)

    # Custom styling
    custom_config = RenderConfig(
        wall_internal=ElementStyle(fill="#1a1a3e", stroke="#0f0f23"),
        door_stroke="#cc0000",
        window_fill="#c0ffc0"
    )
    fp.generate_svg("room_styled.svg", config=custom_config)
```

## Additional Documentation

- **MODULE_STRUCTURE.md**: Detailed module architecture and design decisions
- **RENDERING_GUIDE.md**: Comprehensive guide to styling and rendering
- **VVLM_PROMPT.md**: Prompt template for AI-assisted floorplan generation
