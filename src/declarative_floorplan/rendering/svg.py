"""SVG rendering engine."""

from typing import Tuple

from declarative_floorplan.core.floorplan import Floorplan


class SVGRenderer:
    """Renders floorplans to SVG format."""

    def __init__(self, floorplan: Floorplan) -> None:
        """
        Initialize the SVG renderer.

        Args:
            floorplan: Floorplan to render
        """
        self.floorplan = floorplan

    def render(self) -> str:
        """
        Generate complete SVG document.

        Returns:
            SVG string
        """
        # Calculate viewBox
        viewbox = self._calculate_viewbox()

        # Render elements
        walls_svg = self._render_walls()
        openings_svg = self._render_openings()

        # Build SVG document
        svg = f'<?xml version="1.0" encoding="UTF-8"?>\n'
        svg += f'<svg xmlns="http://www.w3.org/2000/svg" '
        svg += f'viewBox="{viewbox[0]} {viewbox[1]} {viewbox[2]} {viewbox[3]}">\n'
        svg += f'  <title>{self.floorplan.name}</title>\n'
        svg += f'  <g id="walls">\n'
        svg += walls_svg
        svg += f'  </g>\n'
        svg += f'  <g id="openings">\n'
        svg += openings_svg
        svg += f'  </g>\n'
        svg += f'</svg>'

        return svg

    def _calculate_viewbox(self) -> Tuple[float, float, float, float]:
        """
        Calculate the viewBox for the SVG.

        Returns:
            Tuple of (min_x, min_y, width, height)
        """
        vertices = self.floorplan.registry.get_vertices()

        if not vertices:
            return (0, 0, 100, 100)

        positions = [v.get_position() for v in vertices]
        xs = [p[0] for p in positions]
        ys = [p[1] for p in positions]

        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        # Add padding
        padding = 20
        width = max_x - min_x + 2 * padding
        height = max_y - min_y + 2 * padding

        return (min_x - padding, min_y - padding, width, height)

    def _render_walls(self) -> str:
        """
        Render all walls.

        Returns:
            SVG string for walls
        """
        walls = self.floorplan.registry.get_walls()
        svg = ""

        for wall in walls:
            svg += f"    {wall.to_svg()}\n"

        return svg

    def _render_openings(self) -> str:
        """
        Render all doors and windows.

        Returns:
            SVG string for openings
        """
        doors = self.floorplan.registry.get_doors()
        windows = self.floorplan.registry.get_windows()

        svg = ""

        for door in doors:
            svg += f"    {door.to_svg()}\n"

        for window in windows:
            svg += f"    {window.to_svg()}\n"

        return svg
