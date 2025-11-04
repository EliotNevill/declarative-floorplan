#!/usr/bin/env python3
"""
Test script for generating overlays for all examples.

This script:
1. Finds all examples with both model.py and input.png
2. Loads the floorplan from each model.py
3. Generates constraint overlay (constraints on original image)
4. Generates floorplan overlay (rendered floorplan on original image)
"""

import sys
from pathlib import Path

from visual_cot_mcp import (
    load_floorplan_from_model,
    extract_constraints_from_floorplan,
    draw_constraints_on_image,
    overlay_floorplan_on_image,
)


def find_examples_with_images(examples_dir: Path) -> list[Path]:
    """
    Find all example directories that have both model.py and input.png.

    Args:
        examples_dir: Path to the examples directory

    Returns:
        List of paths to example directories
    """
    examples = []

    for example_dir in examples_dir.iterdir():
        if not example_dir.is_dir():
            continue

        model_file = example_dir / "model.py"
        input_image = example_dir / "input.png"

        if model_file.exists() and input_image.exists():
            examples.append(example_dir)

    return sorted(examples)


def process_example(example_dir: Path) -> bool:
    """
    Process a single example: generate constraint and floorplan overlays.

    Args:
        example_dir: Path to the example directory

    Returns:
        True if successful, False otherwise
    """
    example_name = example_dir.name
    model_file = example_dir / "model.py"
    input_image = example_dir / "input.png"

    print(f"\n{'=' * 60}")
    print(f"Processing: {example_name}")
    print(f"{'=' * 60}")

    # Load floorplan from model
    print("\n1. Loading floorplan from model.py...")
    try:
        floorplan = load_floorplan_from_model(str(model_file))
        print(f"   ✓ Loaded: {floorplan}")
    except Exception as e:
        print(f"   ✗ Error loading floorplan: {e}")
        return False

    # Extract constraints from floorplan
    print("\n2. Extracting constraints from floorplan...")
    try:
        constraints = extract_constraints_from_floorplan(floorplan)
        h_count = len(constraints['horizontal'])
        v_count = len(constraints['vertical'])
        print(f"   ✓ Found {h_count} horizontal and {v_count} vertical constraints")
    except Exception as e:
        print(f"   ✗ Error extracting constraints: {e}")
        return False

    # Draw constraints on image
    print("\n3. Drawing constraints overlay...")
    try:
        constraints_output = example_dir / "constraints_overlay.png"
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
        print(f"   ✓ Saved to: {constraints_output.name}")
    except Exception as e:
        print(f"   ✗ Error drawing constraints: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Overlay rendered floorplan
    print("\n4. Drawing floorplan overlay...")
    try:
        overlay_output = example_dir / "floorplan_overlay.png"
        result = overlay_floorplan_on_image(
            floorplan=floorplan,
            image_path=str(input_image),
            overlay_opacity=0.6
        )
        result.save(str(overlay_output))
        print(f"   ✓ Saved to: {overlay_output.name}")
    except Exception as e:
        print(f"   ✗ Error overlaying floorplan: {e}")
        import traceback
        traceback.print_exc()
        return False

    print(f"\n✅ Successfully processed {example_name}")
    return True


def main():
    """Main entry point."""
    # Find the project root (where this script is located)
    project_root = Path(__file__).parent.parent.parent
    examples_dir = project_root / "examples"

    if not examples_dir.exists():
        print(f"Error: Examples directory not found: {examples_dir}")
        sys.exit(1)

    # Find all examples with images
    examples = find_examples_with_images(examples_dir)

    if not examples:
        print("No examples found with both model.py and input.png")
        sys.exit(1)

    print(f"Found {len(examples)} example(s) with input images:")
    for example in examples:
        print(f"  - {example.name}")

    # Process each example
    success_count = 0
    error_count = 0

    for example_dir in examples:
        try:
            if process_example(example_dir):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"\n✗ Unexpected error processing {example_dir.name}: {e}")
            import traceback
            traceback.print_exc()
            error_count += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Summary: {success_count} succeeded, {error_count} failed")
    print("=" * 60)

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
