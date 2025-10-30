"""SVG rendering engine."""

import math
from typing import Optional, Tuple

from declarative_floorplan.core.floorplan import Floorplan
from declarative_floorplan.elements.door import Door
from declarative_floorplan.elements.wall import Wall
from declarative_floorplan.elements.window import Window
from declarative_floorplan.rendering.styles import DEFAULT_CONFIG, RenderConfig


class SVGRenderer:
    """Renders floorplans to SVG format."""

    def __init__(
        self, floorplan: Floorplan, config: Optional[RenderConfig] = None
    ) -> None:
        """
        Initialize the SVG renderer.

        Args:
            floorplan: Floorplan to render
            config: Rendering configuration (uses default if None)
        """
        self.floorplan = floorplan
        self.config = config or DEFAULT_CONFIG

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
        # Add white background
        svg += f'  <rect x="{viewbox[0]}" y="{viewbox[1]}" width="{viewbox[2]}" height="{viewbox[3]}" fill="#ffffff"/>\n'
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
        padding = self.config.viewbox_padding
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
            svg += f"    {self._render_wall(wall)}\n"

        return svg

    def _render_wall(self, wall: Wall) -> str:
        """
        Render a single wall.

        Args:
            wall: Wall to render

        Returns:
            SVG string for the wall
        """
        p1 = wall.start_vertex.get_position()
        p2 = wall.end_vertex.get_position()

        # Calculate wall angle and perpendicular
        angle = wall.angle()
        perp_angle = angle + math.pi / 2
        half_thick = wall.thickness / 2

        # Extend wall along its length by half thickness at each end
        # This ensures proper corner joins
        extend_x = half_thick * math.cos(angle)
        extend_y = half_thick * math.sin(angle)

        # Extended start and end points
        p1_extended = (p1[0] - extend_x, p1[1] - extend_y)
        p2_extended = (p2[0] + extend_x, p2[1] + extend_y)

        # Calculate perpendicular offsets for wall thickness
        offset_x = half_thick * math.cos(perp_angle)
        offset_y = half_thick * math.sin(perp_angle)

        # Four corners of the wall rectangle (using extended points)
        c1 = (p1_extended[0] - offset_x, p1_extended[1] - offset_y)
        c2 = (p1_extended[0] + offset_x, p1_extended[1] + offset_y)
        c3 = (p2_extended[0] + offset_x, p2_extended[1] + offset_y)
        c4 = (p2_extended[0] - offset_x, p2_extended[1] - offset_y)

        points = f"{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {c3[0]:.2f},{c3[1]:.2f} {c4[0]:.2f},{c4[1]:.2f}"

        # Use configured style
        style = self.config.wall_internal
        return f'<polygon points="{points}" {style.to_svg_attrs()}/>'

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
            svg += f"    {self._render_door(door)}\n"

        for window in windows:
            svg += f"    {self._render_window(window)}\n"

        return svg

    def _render_door(self, door: Door) -> str:
        """
        Render a single door.

        Args:
            door: Door to render

        Returns:
            SVG string for the door
        """
        start_point, end_point = door.get_start_end_points()

        # Create the door opening (gap in wall)
        svg = f'<line x1="{start_point[0]:.2f}" y1="{start_point[1]:.2f}" '
        svg += f'x2="{end_point[0]:.2f}" y2="{end_point[1]:.2f}" '
        svg += f'stroke="{self.config.door_fill}" stroke-width="{self.config.door_stroke_width}" />\n'

        # Add door swing arc
        wall_angle = door.wall.angle()
        swing_radius = door.width

        # Convert swing angle to radians
        swing_rad = math.radians(door.swing_angle)

        # Calculate arc start and end angles
        arc_start_angle = wall_angle
        arc_end_angle = wall_angle + swing_rad

        # Create SVG arc path
        start_x = start_point[0]
        start_y = start_point[1]

        # Calculate end point of arc
        end_arc_x = start_x + swing_radius * math.cos(arc_end_angle)
        end_arc_y = start_y + swing_radius * math.sin(arc_end_angle)

        # Determine large arc flag (1 if > 180 degrees)
        large_arc = 1 if abs(door.swing_angle) > 180 else 0

        # SVG path for arc
        svg += f'<path d="M {start_x:.2f},{start_y:.2f} '
        svg += f'A {swing_radius:.2f},{swing_radius:.2f} 0 {large_arc},1 {end_arc_x:.2f},{end_arc_y:.2f}" '
        svg += f'fill="none" stroke="{self.config.door_arc_stroke}" stroke-width="{self.config.door_arc_stroke_width}" />\n'

        # Add door panel line
        svg += f'<line x1="{start_x:.2f}" y1="{start_y:.2f}" '
        svg += f'x2="{end_arc_x:.2f}" y2="{end_arc_y:.2f}" '
        svg += f'stroke="{self.config.door_stroke}" stroke-width="{self.config.door_stroke_width}" />'

        return svg

    def _render_window(self, window: Window) -> str:
        """
        Render a single window.

        Args:
            window: Window to render

        Returns:
            SVG string for the window
        """
        start_point, end_point = window.get_start_end_points()

        # Get perpendicular offsets for window depth
        wall_angle = window.wall.angle()
        perp_angle = wall_angle + math.pi / 2
        half_depth = window.depth / 2

        # Calculate four corners of window rectangle
        offset_x = half_depth * math.cos(perp_angle)
        offset_y = half_depth * math.sin(perp_angle)

        c1 = (start_point[0] - offset_x, start_point[1] - offset_y)
        c2 = (start_point[0] + offset_x, start_point[1] + offset_y)
        c3 = (end_point[0] + offset_x, end_point[1] + offset_y)
        c4 = (end_point[0] - offset_x, end_point[1] - offset_y)

        points = f"{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {c3[0]:.2f},{c3[1]:.2f} {c4[0]:.2f},{c4[1]:.2f}"

        # Create window rectangle
        style = self.config.get_window_style()
        svg = f'<polygon points="{points}" {style.to_svg_attrs()} />\n'

        # Add glass pane lines
        svg += f'<line x1="{start_point[0]:.2f}" y1="{start_point[1]:.2f}" '
        svg += f'x2="{end_point[0]:.2f}" y2="{end_point[1]:.2f}" '
        svg += f'stroke="{self.config.window_glass_stroke}" stroke-width="{self.config.window_glass_stroke_width}" />'

        return svg
