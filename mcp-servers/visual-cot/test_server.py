#!/usr/bin/env python3
"""
Test script for the visual-cot MCP server.

This script tests the draw_constraints functionality directly without
needing to run the full MCP server.
"""

import sys
from pathlib import Path

from visual_cot_mcp import parse_constraints_from_file, draw_constraints_on_image


def test_draw_constraints():
    """Test drawing constraints on the real apartment example."""

    # Use the real apartment example (relative to project root)
    project_root = Path(__file__).parent.parent.parent
    example_dir = project_root / "examples" / "real_apartment"
    model_file = example_dir / "model.py"
    input_image = example_dir / "input.png"
    output_image = example_dir / "constraints_overlay.png"

    if not model_file.exists():
        print(f"Error: Model file not found: {model_file}")
        return False

    if not input_image.exists():
        print(f"Error: Input image not found: {input_image}")
        return False

    print(f"Parsing constraints from: {model_file}")
    constraints = parse_constraints_from_file(str(model_file))

    print(f"Found {len(constraints['horizontal'])} horizontal constraints:")
    for var, coord in constraints['horizontal']:
        print(f"  {var} = {coord}")

    print(f"\nFound {len(constraints['vertical'])} vertical constraints:")
    for var, coord in constraints['vertical']:
        print(f"  {var} = {coord}")

    print(f"\nDrawing constraints on: {input_image}")
    result = draw_constraints_on_image(
        image_path=str(input_image),
        constraints=constraints,
        draw_horizontal=True,
        draw_vertical=True,
        line_color="red",
        line_width=2,
        show_labels=True
    )

    print(f"Saving result to: {output_image}")
    result.save(str(output_image))

    print(f"\nSuccess! Annotated image saved to {output_image}")
    return True


if __name__ == "__main__":
    success = test_draw_constraints()
    sys.exit(0 if success else 1)
