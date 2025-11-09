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

import base64
from io import BytesIO
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent

# Import overlay functions from declarative_floorplan
from declarative_floorplan.rendering.overlays import (
    load_floorplan_from_model,
    draw_constraints_on_image,
    overlay_floorplan_on_image,
)
from declarative_floorplan.geometry.constraints import HorizontalConstraint, VerticalConstraint


# Initialize the MCP server
app = Server("visual-cot")


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

            # Count constraints using registry
            all_constraints = floorplan.registry.get_constraints()
            h_count = sum(1 for c in all_constraints if isinstance(c, HorizontalConstraint)) if draw_horizontal else 0
            v_count = sum(1 for c in all_constraints if isinstance(c, VerticalConstraint)) if draw_vertical else 0

            # Draw constraints on image using SVGRenderer
            result_image = draw_constraints_on_image(
                floorplan=floorplan,
                image_path=image_path,
                output_path=output_path,
                draw_horizontal=draw_horizontal,
                draw_vertical=draw_vertical
            )

            # Build saved message
            saved_msg = f"\nSaved annotated image to: {output_path}" if output_path else ""

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
                output_path=output_path,
                overlay_opacity=overlay_opacity
            )

            # Build saved message
            saved_msg = f"\nSaved overlaid image to: {output_path}" if output_path else ""

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
