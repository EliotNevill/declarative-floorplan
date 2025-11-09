#!/usr/bin/env python3
"""
Render all example floorplans to PNG with optional overlays.

This script:
1. Finds all model.py files in the examples directory
2. Imports the Floorplan object from each model.py
3. Renders the floorplan to SVG and PNG
4. Optionally generates constraint overlays (constraints on image)
5. Optionally generates floorplan overlays (rendered floorplan on original image)
"""

import sys
from pathlib import Path

from PIL import Image
from declarative_floorplan.rendering.svg import SVGRenderer
from declarative_floorplan.rendering.raster import RasterRenderer

# Import overlay functions from overlays module
from declarative_floorplan.rendering.overlays import (
    load_floorplan_from_model,
    draw_constraints_on_image,
    overlay_floorplan_on_image,
)
from declarative_floorplan.geometry.constraints import HorizontalConstraint, VerticalConstraint


def find_example_models(examples_dir: Path) -> list[Path]:
    """
    Find all model.py files in the examples directory.

    Args:
        examples_dir: Path to the examples directory

    Returns:
        List of paths to model.py files
    """
    return list(examples_dir.rglob("model.py"))


def render_floorplan_to_png(floorplan, output_path: Path) -> Image.Image:
    """
    Render a floorplan to PNG using RasterRenderer.

    Args:
        floorplan: The Floorplan object
        output_path: Path where the PNG should be saved

    Returns:
        PIL Image of the rendered floorplan
    """
    # Create renderers
    svg_renderer = SVGRenderer(floorplan)
    raster_renderer = RasterRenderer(svg_renderer)

    # Render to PIL Image and save
    image = raster_renderer.render(background_color='white')
    image.save(str(output_path))

    print(f"✓ Rendered PNG: {output_path} ({image.width}x{image.height})")
    return image


def generate_overlays(floorplan, example_dir: Path) -> None:
    """
    Generate constraint and floorplan overlays for an example.

    Args:
        floorplan: The Floorplan object
        example_dir: Path to the example directory
    """
    input_image = example_dir / "input.png"
    has_input_image = input_image.exists()

    # Count constraints using registry
    all_constraints = floorplan.registry.get_constraints()
    h_count = sum(1 for c in all_constraints if isinstance(c, HorizontalConstraint))
    v_count = sum(1 for c in all_constraints if isinstance(c, VerticalConstraint))

    if h_count == 0 and v_count == 0:
        print("  ⊘ No constraints found, skipping overlay generation")
        return

    print(f"  Found {h_count} horizontal and {v_count} vertical constraints")

    # Determine base image for constraints overlay
    if has_input_image:
        base_image_path = input_image
        base_image_desc = "input image"
    else:
        # Use the rendered output as base
        base_image_path = example_dir / "output.png"
        base_image_desc = "rendered output"

        if not base_image_path.exists():
            print("  ⊘ No base image available for overlays")
            return

    # Generate constraints overlay
    try:
        constraints_output = example_dir / "constraints_overlay.png"
        result = draw_constraints_on_image(
            floorplan=floorplan,
            image_path=str(base_image_path),
            draw_horizontal=True,
            draw_vertical=True
        )
        result.save(str(constraints_output))
        print(f"✓ Constraints overlay: {constraints_output.name} (on {base_image_desc})")
    except Exception as e:
        print(f"✗ Error generating constraints overlay: {e}")

    # Generate floorplan overlay (only if we have an input image)
    if has_input_image:
        try:
            overlay_output = example_dir / "floorplan_overlay.png"
            result = overlay_floorplan_on_image(
                floorplan=floorplan,
                image_path=str(input_image),
                overlay_opacity=0.6
            )
            result.save(str(overlay_output))
            print(f"✓ Floorplan overlay: {overlay_output.name}")
        except Exception as e:
            print(f"✗ Error generating floorplan overlay: {e}")


def main():
    """Main entry point."""
    # Find the project root (where this script is located)
    project_root = Path(__file__).parent
    examples_dir = project_root / "examples"

    if not examples_dir.exists():
        print(f"Error: Examples directory not found: {examples_dir}")
        sys.exit(1)

    # Find all model.py files
    model_files = find_example_models(examples_dir)

    if not model_files:
        print("No model.py files found in examples directory")
        sys.exit(1)

    # Count examples with input images
    examples_with_images = sum(1 for model in model_files if (model.parent / "input.png").exists())

    print(f"Found {len(model_files)} example(s) to render:")
    print(f"  - {examples_with_images} with input images (will generate overlays)")
    print(f"  - {len(model_files) - examples_with_images} without input images")
    print()

    # Process each example
    success_count = 0
    error_count = 0

    for model_path in sorted(model_files):
        example_name = model_path.parent.name
        example_dir = model_path.parent
        has_input = "✓" if (example_dir / "input.png").exists() else "✗"

        print(f"Processing: {example_name} {has_input}")

        try:
            # Load the floorplan
            floorplan = load_floorplan_from_model(model_path)

            # Generate output paths
            svg_output = example_dir / "output.svg"
            png_output = example_dir / "output.png"

            # Render SVG
            floorplan.generate_svg(str(svg_output))
            print(f"✓ Rendered SVG: {svg_output.name}")

            # Render PNG
            render_floorplan_to_png(floorplan, png_output)

            # Generate overlays
            generate_overlays(floorplan, example_dir)

            success_count += 1

        except Exception as e:
            print(f"✗ Error processing {example_name}: {e}")
            import traceback
            traceback.print_exc()
            error_count += 1

        print()  # Blank line between examples

    # Summary
    print("=" * 60)
    print(f"Summary: {success_count} succeeded, {error_count} failed")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
