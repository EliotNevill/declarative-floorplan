#!/usr/bin/env python3
"""
Test script for generating overlays for all examples.

This script:
1. Finds all examples with model.py
2. Loads the floorplan from each model.py
3. Generates constraint overlay (constraints on image)
   - Uses input.png if available, otherwise uses rendered output.png
4. Generates floorplan overlay (rendered floorplan on original image)
   - Only if input.png is available
"""

import sys
from pathlib import Path
from PIL import Image
from io import BytesIO

from visual_cot_mcp import (
    load_floorplan_from_model,
    extract_constraints_from_floorplan,
    draw_constraints_on_image,
    overlay_floorplan_on_image,
)


def find_examples(examples_dir: Path) -> list[Path]:
    """
    Find all example directories that have model.py.

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

        if model_file.exists():
            examples.append(example_dir)

    return sorted(examples)


def render_floorplan_to_image(floorplan) -> Image.Image:
    """
    Render a floorplan to a PIL Image.

    Args:
        floorplan: The Floorplan object

    Returns:
        PIL Image of the rendered floorplan
    """
    from declarative_floorplan.rendering.svg import SVGRenderer
    import cairosvg
    import re

    # Render the floorplan to SVG
    renderer = SVGRenderer(floorplan)
    svg_content = renderer.render()

    # Extract viewBox dimensions from SVG to maintain aspect ratio
    viewbox_match = re.search(r'viewBox="([^"]+)"', svg_content)

    if viewbox_match:
        # Parse viewBox: "x y width height"
        viewbox_parts = viewbox_match.group(1).split()
        if len(viewbox_parts) == 4:
            vb_width = float(viewbox_parts[2])
            vb_height = float(viewbox_parts[3])

            # Scale to a reasonable size while maintaining aspect ratio
            # Target max dimension of 1200px
            max_dimension = 1200
            scale = min(max_dimension / vb_width, max_dimension / vb_height)

            output_width = int(vb_width * scale)
            output_height = int(vb_height * scale)
        else:
            # Fallback to default
            output_width = 1200
            output_height = None
    else:
        # Fallback to default
        output_width = 1200
        output_height = None

    # Convert SVG to PNG
    png_bytes = cairosvg.svg2png(
        bytestring=svg_content.encode('utf-8'),
        output_width=output_width,
        output_height=output_height
    )

    # Load as PIL Image
    return Image.open(BytesIO(png_bytes))


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
    has_input_image = input_image.exists()

    print(f"\n{'=' * 60}")
    print(f"Processing: {example_name}")
    if has_input_image:
        print("  (with input image)")
    else:
        print("  (no input image - will use rendered output)")
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

    # Determine base image for constraints overlay
    if has_input_image:
        base_image_path = input_image
        base_image_desc = "input image"
    else:
        # Render the floorplan first and use it as base
        print("\n3. Rendering floorplan (no input image available)...")
        try:
            rendered_image = render_floorplan_to_image(floorplan)
            temp_base_path = example_dir / "output.png"
            rendered_image.save(str(temp_base_path))
            base_image_path = temp_base_path
            base_image_desc = "rendered output"
            print(f"   ✓ Rendered to: {temp_base_path.name}")
        except Exception as e:
            print(f"   ✗ Error rendering floorplan: {e}")
            import traceback
            traceback.print_exc()
            return False

    # Draw constraints on image
    step_num = 4 if not has_input_image else 3
    print(f"\n{step_num}. Drawing constraints overlay (on {base_image_desc})...")
    try:
        constraints_output = example_dir / "constraints_overlay.png"
        result = draw_constraints_on_image(
            image_path=str(base_image_path),
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

    # Overlay rendered floorplan (only if we have an input image)
    if has_input_image:
        step_num += 1
        print(f"\n{step_num}. Drawing floorplan overlay (on input image)...")
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
    else:
        print("\n   ⊘ Skipping floorplan overlay (no input image)")

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

    # Find all examples with model.py
    examples = find_examples(examples_dir)

    if not examples:
        print("No examples found with model.py")
        sys.exit(1)

    # Count how many have input images
    examples_with_images = sum(1 for ex in examples if (ex / "input.png").exists())

    print(f"Found {len(examples)} example(s) with model.py:")
    print(f"  - {examples_with_images} with input images")
    print(f"  - {len(examples) - examples_with_images} without input images")
    print()
    for example in examples:
        has_input = "✓" if (example / "input.png").exists() else "✗"
        print(f"  {has_input} {example.name}")

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
