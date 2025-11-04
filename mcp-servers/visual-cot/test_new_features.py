#!/usr/bin/env python3
"""
Test script for the updated MCP server features.

This tests:
1. Loading floorplan from model.py
2. Extracting constraints from the loaded floorplan
3. Drawing constraints using the new approach
4. Overlaying the rendered floorplan on the image
"""

import sys
from pathlib import Path

from visual_cot_mcp import (
    load_floorplan_from_model,
    extract_constraints_from_floorplan,
    draw_constraints_on_image,
    overlay_floorplan_on_image,
)


def test_all_features():
    """Test all new MCP server features."""

    # Use the real_apartment example (has input.png)
    project_root = Path(__file__).parent.parent.parent
    example_dir = project_root / "examples" / "real_apartment"
    model_file = example_dir / "model.py"
    input_image = example_dir / "input.png"

    if not model_file.exists():
        print(f"Error: Model file not found: {model_file}")
        return False

    if not input_image.exists():
        print(f"Error: Input image not found: {input_image}")
        print(f"Note: You need to create an input.png file in {example_dir}")
        return False

    print("=" * 60)
    print("Testing MCP Server New Features")
    print("=" * 60)

    # Test 1: Load floorplan from model
    print("\n1. Loading floorplan from model.py...")
    try:
        floorplan = load_floorplan_from_model(str(model_file))
        print(f"   ✓ Loaded: {floorplan}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

    # Test 2: Extract constraints from floorplan
    print("\n2. Extracting constraints from floorplan...")
    try:
        constraints = extract_constraints_from_floorplan(floorplan)
        h_count = len(constraints['horizontal'])
        v_count = len(constraints['vertical'])
        print(f"   ✓ Found {h_count} horizontal and {v_count} vertical constraints")

        print("\n   Horizontal constraints:")
        for var, coord in constraints['horizontal']:
            print(f"     {var} = {coord}")

        print("\n   Vertical constraints:")
        for var, coord in constraints['vertical']:
            print(f"     {var} = {coord}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

    # Test 3: Draw constraints on image
    print("\n3. Drawing constraints on image...")
    try:
        constraints_output = example_dir / "test_constraints.png"
        result = draw_constraints_on_image(
            image_path=str(input_image),
            constraints=constraints,
            draw_horizontal=True,
            draw_vertical=True,
            line_color="red",
            line_width=2,
            show_labels=True
        )
        result.save(str(constraints_output))
        print(f"   ✓ Saved to: {constraints_output}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 4: Overlay rendered floorplan
    print("\n4. Overlaying rendered floorplan on image...")
    try:
        overlay_output = example_dir / "test_overlay.png"
        result = overlay_floorplan_on_image(
            floorplan=floorplan,
            image_path=str(input_image),
            overlay_opacity=0.6
        )
        result.save(str(overlay_output))
        print(f"   ✓ Saved to: {overlay_output}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_all_features()
    sys.exit(0 if success else 1)
