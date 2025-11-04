#!/usr/bin/env python3
"""
Render all example floorplans to PNG.

This script:
1. Finds all model.py files in the examples directory
2. Imports the Floorplan object from each model.py
3. Renders the floorplan to SVG
4. Converts the SVG to PNG using cairosvg
"""

import sys
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

import cairosvg
from declarative_floorplan.rendering.svg import SVGRenderer


def find_example_models(examples_dir: Path) -> list[Path]:
    """
    Find all model.py files in the examples directory.

    Args:
        examples_dir: Path to the examples directory

    Returns:
        List of paths to model.py files
    """
    return list(examples_dir.rglob("model.py"))


def load_floorplan_from_model(model_path: Path):
    """
    Import a model.py file and extract the Floorplan object.

    Args:
        model_path: Path to the model.py file

    Returns:
        The Floorplan object (variable name 'fp' by convention)
    """
    # Create a unique module name based on the path
    module_name = f"model_{model_path.parent.name}"

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
    from declarative_floorplan import Floorplan
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, Floorplan):
            return attr

    raise ValueError(f"No Floorplan object found in {model_path}")


def render_floorplan_to_png(floorplan, output_path: Path) -> None:
    """
    Render a floorplan to PNG.

    Args:
        floorplan: The Floorplan object
        output_path: Path where the PNG should be saved
    """
    # Generate SVG string
    renderer = SVGRenderer(floorplan)
    svg_content = renderer.render()

    # Extract viewBox dimensions from SVG to maintain aspect ratio
    import re
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

    # Convert SVG to PNG using cairosvg
    cairosvg.svg2png(
        bytestring=svg_content.encode('utf-8'),
        write_to=str(output_path),
        output_width=output_width,
        output_height=output_height,
        background_color='white'
    )

    print(f"✓ Rendered: {output_path} ({output_width}x{output_height})")


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

    print(f"Found {len(model_files)} example(s) to render:\n")

    # Process each example
    success_count = 0
    error_count = 0

    for model_path in sorted(model_files):
        example_name = model_path.parent.name
        print(f"Processing: {example_name}")

        try:
            # Load the floorplan
            floorplan = load_floorplan_from_model(model_path)

            # Generate output paths
            svg_output = model_path.parent / "output.svg"
            png_output = model_path.parent / "output.png"

            # Render SVG
            floorplan.generate_svg(str(svg_output))

            # Render PNG
            render_floorplan_to_png(floorplan, png_output)

            success_count += 1

        except Exception as e:
            print(f"✗ Error processing {example_name}: {e}")
            error_count += 1

        print()  # Blank line between examples

    # Summary
    print("=" * 60)
    print(f"Summary: {success_count} succeeded, {error_count} failed")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
