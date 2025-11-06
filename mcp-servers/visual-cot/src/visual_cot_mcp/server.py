#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mcp>=0.9.0",
#   "pillow>=10.0.0",
# ]
# ///

"""
Visual Chain of Thought MCP Server

This MCP server provides tools to visualize floorplan generation steps
by overlaying constraints and other elements on the original image.
"""

import ast
import base64
import re
import sys
from io import BytesIO
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent
from PIL import Image


# Initialize the MCP server
app = Server("visual-cot")


def load_floorplan_from_model(model_path: str):
    """
    Import a model.py file and extract the Floorplan object.

    Args:
        model_path: Path to the model.py file

    Returns:
        The Floorplan object (variable name 'fp' by convention)
    """
    from declarative_floorplan import Floorplan

    model_path_obj = Path(model_path)

    # Create a unique module name based on the path
    module_name = f"model_{model_path_obj.parent.name}_{id(model_path)}"

    # Load the module
    spec = spec_from_file_location(module_name, model_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {model_path}")

    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Look for the Floorplan object (usually named 'fp')
    if hasattr(module, 'fp'):
        return module.fp

    # Fallback: search for any Floorplan instance
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, Floorplan):
            return attr

    raise ValueError(f"No Floorplan object found in {model_path}")


def parse_constraints_from_file(file_path: str) -> dict[str, list[tuple[str, int]]]:
    """
    Parse a Python model file to extract constraint definitions.

    Returns a dict with 'horizontal' and 'vertical' keys, each containing
    a list of (variable_name, coordinate) tuples.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    constraints = {
        'horizontal': [],
        'vertical': []
    }

    # Parse using AST for more robust extraction
    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                # Check if this is a constraint assignment
                if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    var_name = node.targets[0].id

                    # Check for HC(value) or HorizontalConstraint(value)
                    if isinstance(node.value, ast.Call):
                        if isinstance(node.value.func, ast.Name):
                            func_name = node.value.func.id

                            if func_name in ['HC', 'HorizontalConstraint']:
                                if len(node.value.args) > 0 and isinstance(node.value.args[0], ast.Constant):
                                    y_coord = node.value.args[0].value
                                    constraints['horizontal'].append((var_name, y_coord))

                            elif func_name in ['VC', 'VerticalConstraint']:
                                if len(node.value.args) > 0 and isinstance(node.value.args[0], ast.Constant):
                                    x_coord = node.value.args[0].value
                                    constraints['vertical'].append((var_name, x_coord))
    except SyntaxError:
        # Fallback to regex if AST parsing fails
        h_pattern = r'(\w+)\s*=\s*HC\((\d+)\)'
        v_pattern = r'(\w+)\s*=\s*VC\((\d+)\)'

        for match in re.finditer(h_pattern, content):
            var_name, y_coord = match.groups()
            constraints['horizontal'].append((var_name, int(y_coord)))

        for match in re.finditer(v_pattern, content):
            var_name, x_coord = match.groups()
            constraints['vertical'].append((var_name, int(x_coord)))

    return constraints


def extract_constraints_from_floorplan(floorplan) -> dict[str, list[tuple[str, int]]]:
    """
    Extract constraints from a loaded Floorplan object.

    Args:
        floorplan: The Floorplan object

    Returns:
        Dict with 'horizontal' and 'vertical' constraint lists
    """
    from declarative_floorplan.geometry.constraints import HorizontalConstraint, VerticalConstraint

    constraints = {
        'horizontal': [],
        'vertical': []
    }

    # Get all vertices from the floorplan
    vertices = floorplan.registry.get_vertices()

    # Track unique constraints to avoid duplicates
    seen_h_constraints = set()
    seen_v_constraints = set()

    for vertex in vertices:
        for constraint in vertex.constraints:
            if isinstance(constraint, HorizontalConstraint):
                coord = int(constraint.get_value())
                if coord not in seen_h_constraints:
                    # Use a generic name since we don't have the variable name
                    constraints['horizontal'].append((f"h_{coord}", coord))
                    seen_h_constraints.add(coord)
            elif isinstance(constraint, VerticalConstraint):
                coord = int(constraint.get_value())
                if coord not in seen_v_constraints:
                    constraints['vertical'].append((f"v_{coord}", coord))
                    seen_v_constraints.add(coord)

    return constraints


def draw_constraints_on_image(
    floorplan,
    image_path: str,
    draw_horizontal: bool = True,
    draw_vertical: bool = True,
) -> Image.Image:
    """
    Draw constraints on the image using SVGRenderer and RasterRenderer.

    Args:
        floorplan: The Floorplan object to extract constraints from
        image_path: Path to the base image
        draw_horizontal: Whether to draw horizontal constraints (not currently used)
        draw_vertical: Whether to draw vertical constraints (not currently used)

    Returns:
        PIL Image with constraints drawn
    """
    from declarative_floorplan.rendering.svg import SVGRenderer
    from declarative_floorplan.rendering.raster import RasterRenderer
    from declarative_floorplan.rendering.styles import RenderConfig, RenderMode

    # Load the base image
    base_img = Image.open(image_path).convert('RGBA')

    # Create config for constraints-only rendering with matching dimensions
    config = RenderConfig(
        render_mode=RenderMode.CONSTRAINTS_ONLY,
        viewbox_override=(0, 0, base_img.width, base_img.height)
    )

    # Render constraints using RasterRenderer
    svg_renderer = SVGRenderer(floorplan, config=config)
    raster_renderer = RasterRenderer(svg_renderer)
    constraints_img = raster_renderer.render(background_color=None).convert('RGBA')

    # Composite the constraints layer onto the base image
    result = Image.alpha_composite(base_img, constraints_img)

    return result.convert('RGB')


def overlay_floorplan_on_image(
    floorplan,
    image_path: str,
    overlay_opacity: float = 0.6,
    line_color: str = "blue"
) -> Image.Image:
    """
    Render a floorplan and overlay it on the original image.

    Args:
        floorplan: The Floorplan object to render
        image_path: Path to the base image
        overlay_opacity: Opacity of the floorplan overlay (0.0 to 1.0)
        line_color: Color for the floorplan rendering (not currently used)

    Returns:
        PIL Image with floorplan overlaid
    """
    from declarative_floorplan.rendering.svg import SVGRenderer
    from declarative_floorplan.rendering.raster import RasterRenderer
    from declarative_floorplan.rendering.styles import RenderConfig

    # Load the base image
    base_img = Image.open(image_path).convert('RGBA')

    # Create config with viewbox override to match base image size
    config = RenderConfig(
        viewbox_override=(0, 0, base_img.width, base_img.height)
    )

    # Render the floorplan using RasterRenderer
    svg_renderer = SVGRenderer(floorplan, config=config)
    raster_renderer = RasterRenderer(svg_renderer)
    floorplan_img = raster_renderer.render(background_color=None).convert('RGBA')

    # Adjust opacity of the floorplan
    alpha = floorplan_img.split()[3]
    alpha = alpha.point(lambda p: int(p * overlay_opacity))
    floorplan_img.putalpha(alpha)

    # Composite the floorplan onto the base image
    result = Image.alpha_composite(base_img, floorplan_img)

    return result.convert('RGB')


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="draw_constraints",
            description=(
                "Draw horizontal and/or vertical constraints from a floorplan model file "
                "overlaid on the original image. This helps visualize the constraint "
                "identification step in the floorplan generation process."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file_path": {
                        "type": "string",
                        "description": "Path to the Python model file containing constraint definitions"
                    },
                    "image_path": {
                        "type": "string",
                        "description": "Path to the original floorplan image"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where the annotated image should be saved (optional)",
                        "default": None
                    },
                    "draw_horizontal": {
                        "type": "boolean",
                        "description": "Whether to draw horizontal constraints",
                        "default": True
                    },
                    "draw_vertical": {
                        "type": "boolean",
                        "description": "Whether to draw vertical constraints",
                        "default": True
                    },
                    "line_color": {
                        "type": "string",
                        "description": "Color for constraint lines (default: red)",
                        "default": "red"
                    },
                    "line_width": {
                        "type": "integer",
                        "description": "Width of constraint lines in pixels (default: 2)",
                        "default": 2
                    },
                    "show_labels": {
                        "type": "boolean",
                        "description": "Whether to show constraint labels",
                        "default": True
                    }
                },
                "required": ["model_file_path", "image_path"]
            }
        ),
        Tool(
            name="overlay_floorplan",
            description=(
                "Load a floorplan model, render it, and overlay it on the original image. "
                "This helps visualize the complete generated floorplan compared to the original."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file_path": {
                        "type": "string",
                        "description": "Path to the Python model file containing the Floorplan object"
                    },
                    "image_path": {
                        "type": "string",
                        "description": "Path to the original floorplan image"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where the overlaid image should be saved (optional)",
                        "default": None
                    },
                    "overlay_opacity": {
                        "type": "number",
                        "description": "Opacity of the floorplan overlay (0.0 to 1.0, default: 0.6)",
                        "default": 0.6
                    }
                },
                "required": ["model_file_path", "image_path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent]:
    """Handle tool calls."""

    if name == "draw_constraints":
        model_file_path = arguments["model_file_path"]
        image_path = arguments["image_path"]
        output_path = arguments.get("output_path")
        draw_horizontal = arguments.get("draw_horizontal", True)
        draw_vertical = arguments.get("draw_vertical", True)

        try:
            # Load the floorplan from the model file
            floorplan = load_floorplan_from_model(model_file_path)

            # Extract constraints from the floorplan for counting
            constraints = extract_constraints_from_floorplan(floorplan)

            # Count constraints
            h_count = len(constraints['horizontal']) if draw_horizontal else 0
            v_count = len(constraints['vertical']) if draw_vertical else 0

            # Draw constraints on image using SVGRenderer
            result_image = draw_constraints_on_image(
                floorplan=floorplan,
                image_path=image_path,
                draw_horizontal=draw_horizontal,
                draw_vertical=draw_vertical
            )

            # Save if output path provided
            if output_path:
                result_image.save(output_path)
                saved_msg = f"\nSaved annotated image to: {output_path}"
            else:
                saved_msg = ""

            # Convert image to base64 for returning
            buffered = BytesIO()
            result_image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Create summary text
            summary = (
                f"Drew {h_count} horizontal and {v_count} vertical constraints "
                f"from {model_file_path} on {image_path} using SVGRenderer.{saved_msg}"
            )

            return [
                TextContent(
                    type="text",
                    text=summary
                ),
                ImageContent(
                    type="image",
                    data=img_base64,
                    mimeType="image/png"
                )
            ]

        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]

    elif name == "overlay_floorplan":
        model_file_path = arguments["model_file_path"]
        image_path = arguments["image_path"]
        output_path = arguments.get("output_path")
        overlay_opacity = arguments.get("overlay_opacity", 0.6)

        try:
            # Load the floorplan from the model file
            floorplan = load_floorplan_from_model(model_file_path)

            # Overlay the rendered floorplan on the image
            result_image = overlay_floorplan_on_image(
                floorplan=floorplan,
                image_path=image_path,
                overlay_opacity=overlay_opacity
            )

            # Save if output path provided
            if output_path:
                result_image.save(output_path)
                saved_msg = f"\nSaved overlaid image to: {output_path}"
            else:
                saved_msg = ""

            # Convert image to base64 for returning
            buffered = BytesIO()
            result_image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Create summary text
            summary = (
                f"Overlaid rendered floorplan from {model_file_path} "
                f"on {image_path} (opacity: {overlay_opacity}).{saved_msg}"
            )

            return [
                TextContent(
                    type="text",
                    text=summary
                ),
                ImageContent(
                    type="image",
                    data=img_base64,
                    mimeType="image/png"
                )
            ]

        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]

    raise ValueError(f"Unknown tool: {name}")


async def async_main():
    """Run the MCP server (async implementation)."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def main():
    """Run the MCP server (entry point)."""
    import asyncio
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
