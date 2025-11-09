"""Overlay utilities for visual validation of floorplan models.

This module provides functions to overlay rendered floorplan elements
(constraints, walls, doors, windows) on original floorplan images for
visual comparison and validation.
"""

import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import Optional, Union

try:
    from PIL import Image
except ImportError:
    raise ImportError(
        "PIL (Pillow) is required for overlay functionality. "
        "Install it with: pip install pillow"
    )

from .svg import SVGRenderer
from .raster import RasterRenderer
from .styles import RenderConfig, RenderMode


def load_floorplan_from_model(model_path: Union[str, Path]):
    """Import a model.py file and extract the Floorplan object.

    Args:
        model_path: Path to the model.py file

    Returns:
        The Floorplan object (variable name 'fp' by convention)

    Raises:
        ImportError: If the module cannot be loaded
        ValueError: If no Floorplan object is found in the module
    """
    from declarative_floorplan import Floorplan

    model_path_obj = Path(model_path)

    if not model_path_obj.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

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


def draw_constraints_on_image(
    floorplan,
    image_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    draw_horizontal: bool = True,
    draw_vertical: bool = True,
) -> Image.Image:
    """Draw constraints from a floorplan overlaid on an image.

    This renders only the constraint lines (horizontal and vertical)
    on top of the original floorplan image for visual validation.

    Args:
        floorplan: The Floorplan object to extract constraints from
        image_path: Path to the base/original image
        output_path: Optional path to save the output image
        draw_horizontal: Whether to draw horizontal constraints
        draw_vertical: Whether to draw vertical constraints

    Returns:
        PIL Image with constraints drawn on top of the original

    Example:
        >>> from declarative_floorplan import Floorplan
        >>> from declarative_floorplan.rendering.overlays import draw_constraints_on_image
        >>>
        >>> # Load floorplan from model file
        >>> fp = load_floorplan_from_model("model.py")
        >>>
        >>> # Draw constraints on original image
        >>> result = draw_constraints_on_image(
        ...     floorplan=fp,
        ...     image_path="original.png",
        ...     output_path="constraints_overlay.png"
        ... )
    """
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

    # Save if output path provided
    if output_path:
        result.convert('RGB').save(output_path)

    return result.convert('RGB')


def overlay_floorplan_on_image(
    floorplan,
    image_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    overlay_opacity: float = 0.6,
) -> Image.Image:
    """Render a complete floorplan and overlay it on the original image.

    This renders the entire floorplan (walls, doors, windows, etc.)
    with adjustable opacity on top of the original image for comparison.

    Args:
        floorplan: The Floorplan object to render
        image_path: Path to the base/original image
        output_path: Optional path to save the output image
        overlay_opacity: Opacity of the floorplan overlay (0.0 to 1.0)

    Returns:
        PIL Image with floorplan overlaid on the original

    Example:
        >>> from declarative_floorplan.rendering.overlays import (
        ...     load_floorplan_from_model,
        ...     overlay_floorplan_on_image
        ... )
        >>>
        >>> # Load floorplan from model file
        >>> fp = load_floorplan_from_model("model.py")
        >>>
        >>> # Overlay complete floorplan on original
        >>> result = overlay_floorplan_on_image(
        ...     floorplan=fp,
        ...     image_path="original.png",
        ...     output_path="floorplan_overlay.png",
        ...     overlay_opacity=0.7
        ... )
    """
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

    # Save if output path provided
    if output_path:
        result.convert('RGB').save(output_path)

    return result.convert('RGB')


def draw_constraints_from_model_file(
    model_path: Union[str, Path],
    image_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
) -> Image.Image:
    """Convenience function to draw constraints directly from a model file.

    Args:
        model_path: Path to the Python model file
        image_path: Path to the original floorplan image
        output_path: Optional path to save the output image

    Returns:
        PIL Image with constraints overlaid

    Example:
        >>> from declarative_floorplan.rendering.overlays import draw_constraints_from_model_file
        >>>
        >>> result = draw_constraints_from_model_file(
        ...     model_path="my_floorplan.py",
        ...     image_path="original.png",
        ...     output_path="constraints.png"
        ... )
    """
    floorplan = load_floorplan_from_model(model_path)
    return draw_constraints_on_image(
        floorplan=floorplan,
        image_path=image_path,
        output_path=output_path
    )


def overlay_floorplan_from_model_file(
    model_path: Union[str, Path],
    image_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    overlay_opacity: float = 0.6,
) -> Image.Image:
    """Convenience function to overlay floorplan directly from a model file.

    Args:
        model_path: Path to the Python model file
        image_path: Path to the original floorplan image
        output_path: Optional path to save the output image
        overlay_opacity: Opacity of the floorplan overlay (0.0 to 1.0)

    Returns:
        PIL Image with floorplan overlaid

    Example:
        >>> from declarative_floorplan.rendering.overlays import overlay_floorplan_from_model_file
        >>>
        >>> result = overlay_floorplan_from_model_file(
        ...     model_path="my_floorplan.py",
        ...     image_path="original.png",
        ...     output_path="overlay.png",
        ...     overlay_opacity=0.7
        ... )
    """
    floorplan = load_floorplan_from_model(model_path)
    return overlay_floorplan_on_image(
        floorplan=floorplan,
        image_path=image_path,
        output_path=output_path,
        overlay_opacity=overlay_opacity
    )
