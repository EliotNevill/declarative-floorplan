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
from io import BytesIO
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent
from PIL import Image, ImageDraw, ImageFont


# Initialize the MCP server
app = Server("visual-cot")


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


def draw_constraints_on_image(
    image_path: str,
    constraints: dict[str, list[tuple[str, int]]],
    draw_horizontal: bool = True,
    draw_vertical: bool = True,
    line_color: str = "red",
    line_width: int = 2,
    show_labels: bool = True,
    label_color: str = "red"
) -> Image.Image:
    """
    Draw constraints on the image.

    Args:
        image_path: Path to the base image
        constraints: Dict with 'horizontal' and 'vertical' constraint lists
        draw_horizontal: Whether to draw horizontal constraints
        draw_vertical: Whether to draw vertical constraints
        line_color: Color for constraint lines
        line_width: Width of constraint lines
        show_labels: Whether to show constraint labels
        label_color: Color for constraint labels

    Returns:
        PIL Image with constraints drawn
    """
    # Load the image
    img = Image.open(image_path).convert('RGBA')

    # Create a transparent overlay
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Try to use a better font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Draw horizontal constraints
    if draw_horizontal:
        for var_name, y_coord in constraints['horizontal']:
            # Draw line
            draw.line([(0, y_coord), (img.width, y_coord)], fill=line_color, width=line_width)

            # Draw label
            if show_labels:
                label = f"{var_name} (y={y_coord})"
                # Draw background for text
                bbox = draw.textbbox((5, y_coord + 5), label, font=font)
                draw.rectangle(bbox, fill=(255, 255, 255, 180))
                draw.text((5, y_coord + 5), label, fill=label_color, font=font)

    # Draw vertical constraints
    if draw_vertical:
        for var_name, x_coord in constraints['vertical']:
            # Draw line
            draw.line([(x_coord, 0), (x_coord, img.height)], fill=line_color, width=line_width)

            # Draw label
            if show_labels:
                label = f"{var_name} (x={x_coord})"
                # Draw background for text
                bbox = draw.textbbox((x_coord + 5, 5), label, font=font)
                draw.rectangle(bbox, fill=(255, 255, 255, 180))
                draw.text((x_coord + 5, 5), label, fill=label_color, font=font)

    # Composite the overlay onto the original image
    result = Image.alpha_composite(img, overlay)

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
        line_color = arguments.get("line_color", "red")
        line_width = arguments.get("line_width", 2)
        show_labels = arguments.get("show_labels", True)

        try:
            # Parse constraints from model file
            constraints = parse_constraints_from_file(model_file_path)

            # Count constraints
            h_count = len(constraints['horizontal'])
            v_count = len(constraints['vertical'])

            # Draw constraints on image
            result_image = draw_constraints_on_image(
                image_path=image_path,
                constraints=constraints,
                draw_horizontal=draw_horizontal,
                draw_vertical=draw_vertical,
                line_color=line_color,
                line_width=line_width,
                show_labels=show_labels
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
                f"from {model_file_path} on {image_path}.{saved_msg}"
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


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
