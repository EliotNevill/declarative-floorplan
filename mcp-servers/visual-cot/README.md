# Visual Chain of Thought MCP Server

An MCP (Model Context Protocol) server that provides visual debugging tools for the floorplan generation process. This server helps AI agents visualize constraint identification and other steps when generating floorplan models from images.

## Features

- **draw_constraints**: Overlay horizontal and vertical constraints from a model file onto the original floorplan image
- Returns annotated images to help verify constraint placement
- Supports customizable colors, line widths, and labels

## Installation

### Using uv (recommended)

From the **project root** directory:

```bash
# Install the MCP server (and the main library as an editable dependency)
cd mcp-servers/visual-cot
uv sync

# Or install in the main project's environment
cd /path/to/declarative-floorplan
uv pip install -e mcp-servers/visual-cot
```

### Using pip

```bash
cd mcp-servers/visual-cot
pip install -e .
```

## Usage

### Running the Server

```bash
# From mcp-servers/visual-cot directory
uv run python -m visual_cot_mcp.server

# Or using the installed script
uv run visual-cot-mcp
```

### Testing Locally

Run the test script to verify everything works:

```bash
cd mcp-servers/visual-cot
uv run python test_server.py
```

This will process the `examples/real_apartment` example and generate a `constraints_overlay.png` file.

### Configuring in Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "visual-cot": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/declarative-floorplan/mcp-servers/visual-cot",
        "run",
        "visual-cot-mcp"
      ]
    }
  }
}
```

Replace `/path/to/declarative-floorplan` with the actual path to your project directory.

### Example Tool Call

```python
# From within Claude or another MCP client:
draw_constraints(
    model_file_path="examples/real_apartment/model.py",
    image_path="examples/real_apartment/input.png",
    output_path="examples/real_apartment/constraints_overlay.png",
    draw_horizontal=True,
    draw_vertical=True,
    line_color="red",
    line_width=2,
    show_labels=True
)
```

## Tool Reference

### draw_constraints

Draw horizontal and/or vertical constraints from a floorplan model file overlaid on the original image.

**Parameters:**
- `model_file_path` (required): Path to the Python model file containing constraint definitions
- `image_path` (required): Path to the original floorplan image
- `output_path` (optional): Path where the annotated image should be saved
- `draw_horizontal` (optional, default: true): Whether to draw horizontal constraints
- `draw_vertical` (optional, default: true): Whether to draw vertical constraints
- `line_color` (optional, default: "red"): Color for constraint lines
- `line_width` (optional, default: 2): Width of constraint lines in pixels
- `show_labels` (optional, default: true): Whether to show constraint labels

**Returns:**
- Text summary of what was drawn
- PNG image with constraints overlaid

## Architecture

This MCP server is part of the `declarative-floorplan` monorepo:

```
declarative-floorplan/
├── src/declarative_floorplan/    # Main library
├── mcp-servers/
│   └── visual-cot/               # This MCP server
│       ├── pyproject.toml        # Depends on main library
│       └── src/visual_cot_mcp/
│           └── server.py
└── examples/                      # Shared examples
```

The server depends on the main `declarative-floorplan` library as an editable dependency, allowing it to stay in sync with any changes to the core library.

## How It Works

1. Parses the Python model file using AST to extract `HC()` and `VC()` constraint definitions
2. Loads the original image
3. Draws lines at the specified coordinates (horizontal for HC, vertical for VC)
4. Adds labels showing the variable name and coordinate value
5. Returns the annotated image

This helps agents verify that constraints are being identified correctly in Step 1 of the floorplan generation process (as described in VVLM_PROMPT.md).

## Development

### Running Tests

```bash
cd mcp-servers/visual-cot
uv run python test_server.py
```

### Adding New Tools

To add new visualization tools (e.g., for vertices, walls, doors):

1. Add the function to `src/visual_cot_mcp/server.py`
2. Register it with `@app.list_tools()` and `@app.call_tool()`
3. Update this README with documentation

## Future Extensions

Planned tools for other visualization steps:
- `draw_vertices`: Show vertex positions
- `draw_walls`: Highlight wall connections
- `draw_openings`: Overlay doors and windows
- `draw_full_model`: Complete overlay of the generated model
