"""Raster rendering engine for converting SVG to PNG."""

import re
from io import BytesIO
from typing import Optional

from PIL import Image

from declarative_floorplan.rendering.svg import SVGRenderer


class RasterRenderer:
    """Converts SVG renderings to raster images (PNG)."""

    def __init__(self, svg_renderer: SVGRenderer) -> None:
        """
        Initialize the raster renderer.

        Args:
            svg_renderer: SVGRenderer instance to use for generating SVG content
        """
        self.svg_renderer = svg_renderer

    def render(self, background_color: Optional[str] = 'white') -> Image.Image:
        """
        Render the floorplan to a PIL Image.

        Args:
            background_color: Background color for the image (default: 'white').
                            Use None for transparent background.

        Returns:
            PIL Image object
        """
        import cairosvg

        # Get SVG content from the SVGRenderer
        svg_content = self.svg_renderer.render()

        # Extract viewBox dimensions from SVG to maintain aspect ratio
        viewbox_match = re.search(r'viewBox="([^"]+)"', svg_content)

        if not viewbox_match:
            raise ValueError("SVG content does not contain a viewBox attribute")

        viewbox_parts = viewbox_match.group(1).split()
        _, _, output_width, output_height = map(float, viewbox_parts)

        # Convert SVG to PNG using cairosvg
        png_bytes = cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            output_width=int(output_width),
            output_height=int(output_height),
            background_color=background_color
        )

        # Load PNG bytes into PIL Image
        return Image.open(BytesIO(png_bytes))

    def save(
        self,
        output_path: str,
        background_color: Optional[str] = 'white'
    ) -> None:
        """
        Render and save the floorplan to a file.

        Args:
            output_path: Path where the image should be saved
            background_color: Background color for the image (default: 'white').
                            Use None for transparent background.
        """
        image = self.render(background_color=background_color)
        image.save(output_path)
