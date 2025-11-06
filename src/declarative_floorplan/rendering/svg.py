"""SVG rendering engine."""

import math
from typing import Optional, Tuple

from declarative_floorplan.core.floorplan import Floorplan
from declarative_floorplan.elements.door import Door
from declarative_floorplan.elements.wall import Wall
from declarative_floorplan.elements.window import Window
from declarative_floorplan.geometry.constraints import HorizontalConstraint, VerticalConstraint
from declarative_floorplan.rendering.styles import DEFAULT_CONFIG, RenderConfig, RenderMode


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

        # Build SVG document
        svg = '<?xml version="1.0" encoding="UTF-8"?>\n'
        svg += '<svg xmlns="http://www.w3.org/2000/svg" '
        svg += f'viewBox="{viewbox[0]} {viewbox[1]} {viewbox[2]} {viewbox[3]}">\n'
        svg += f'  <title>{self.floorplan.name}</title>\n'

        # Handle different render modes
        if self.config.render_mode == RenderMode.CONSTRAINTS_ONLY:
            # Render only constraints on transparent background
            constraints_svg = self._render_constraints()
            svg += '  <g id="constraints">\n'
            svg += constraints_svg
            svg += '  </g>\n'
        else:
            # Full rendering: background, walls, openings
            # Add white background
            svg += f'  <rect x="{viewbox[0]}" y="{viewbox[1]}" width="{viewbox[2]}" height="{viewbox[3]}" fill="#ffffff"/>\n'

            # Render elements
            walls_svg = self._render_walls()
            openings_svg = self._render_openings()

            svg += '  <g id="walls">\n'
            svg += walls_svg
            svg += '  </g>\n'
            svg += '  <g id="openings">\n'
            svg += openings_svg
            svg += '  </g>\n'

        svg += '</svg>'

        return svg

    def _calculate_viewbox(self) -> Tuple[float, float, float, float]:
        """
        Calculate the viewBox for the SVG.

        Always starts at (0, 0) to ensure constraint coordinates align correctly.

        Returns:
            Tuple of (0, 0, width, height)
        """
        # Check if viewbox_override is set
        if self.config.viewbox_override is not None:
            return self.config.viewbox_override

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

        # Add padding around the content
        padding = self.config.viewbox_padding

        # Calculate dimensions to include all content plus padding
        # ViewBox always starts at (0, 0) for proper coordinate alignment
        width = max_x + padding
        height = max_y + padding

        # If content doesn't start at 0, we still need to include that space
        # to ensure coordinates are preserved
        if min_x < 0:
            width += abs(min_x)
        if min_y < 0:
            height += abs(min_y)

        return (0, 0, width, height)

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

        # Calculate perpendicular offsets for door thickness
        wall_angle = door.wall.angle()
        perp_angle = wall_angle + math.pi / 2
        half_thick = door.wall.thickness / 2

        # Calculate four corners of threshold
        offset_x = half_thick * math.cos(perp_angle)
        offset_y = half_thick * math.sin(perp_angle)

        c1 = (start_point[0] - offset_x, start_point[1] - offset_y)
        c2 = (start_point[0] + offset_x, start_point[1] + offset_y)
        c3 = (end_point[0] + offset_x, end_point[1] + offset_y)
        c4 = (end_point[0] - offset_x, end_point[1] - offset_y)

        threshold_points = f"{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {c3[0]:.2f},{c3[1]:.2f} {c4[0]:.2f},{c4[1]:.2f}"

        # Start door group
        svg = f'<g id="Door" fill="{self.config.door_fill}" stroke="{self.config.door_stroke}" '
        svg += f'style="fill-opacity: 1; stroke-width: {self.config.door_stroke_width}; stroke-opacity: 1;" '
        svg += 'class="Door">\n'

        # Threshold
        svg += '  <g id="Threshold" class="Threshold">\n'
        svg += f'    <polygon points="{threshold_points}" />\n'
        svg += '  </g>\n'

        # Panel and swing arc
        swing_radius = door.width
        swing_rad = math.radians(door.swing_angle)

        # Calculate hinge point (on the inside edge of the wall)
        hinge_x = start_point[0] + offset_x
        hinge_y = start_point[1] + offset_y

        # <-- FIX 1: Calculate the arc's START point (latch side)
        # This is the 'closed' position of the door's tip.
        arc_start_x = end_point[0] + offset_x
        arc_start_y = end_point[1] + offset_y

        # <-- FIX 2: Calculate the open door angle correctly
        # The 'closed' angle is the wall_angle. The 'open' angle is wall_angle + swing.
        arc_end_angle = wall_angle + swing_rad
        end_arc_x = hinge_x + swing_radius * math.cos(arc_end_angle)
        end_arc_y = hinge_y + swing_radius * math.sin(arc_end_angle)

        # <-- FIX 3: Determine large_arc and sweep_flag
        large_arc = 1 if abs(door.swing_angle) > 180 else 0
        sweep_flag = 1 if door.swing_angle > 0 else 0  # 1 for positive (CCW), 0 for negative (CW)

        # Panel group with swing arc
        svg += '  <g id="Panel" fill="none" class="Panel">\n'
        
        # Arc from latch-side (arc_start) to open-door-tip (end_arc)
        svg += f'    <path d="M {arc_start_x:.2f},{arc_start_y:.2f} '  # <-- FIX 1 (continued)
        svg += f'A {swing_radius:.2f},{swing_radius:.2f} 0 {large_arc},{sweep_flag} {end_arc_x:.2f},{end_arc_y:.2f}" '  # <-- FIX 3 (continued)
        svg += f'stroke="{self.config.door_arc_stroke}" stroke-width="{self.config.door_arc_stroke_width}" />\n'

        # Door panel line in open position (from hinge to open-door-tip)
        svg += f'    <line x1="{hinge_x:.2f}" y1="{hinge_y:.2f}" '
        svg += f'x2="{end_arc_x:.2f}" y2="{end_arc_y:.2f}" '
        svg += f'stroke="{self.config.door_stroke}" stroke-width="{self.config.door_stroke_width}" />\n'
        svg += '  </g>\n'

        svg += '</g>'

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

        # Start window group
        svg = '<g id="Window" class="Window">\n'

        # Create window rectangle (frame)
        style = self.config.get_window_style()
        svg += f'  <polygon points="{points}" {style.to_svg_attrs()} />\n'

        # Add multiple glass pane lines (parallel lines to show glass panes)
        # Center line
        svg += f'  <line x1="{start_point[0]:.2f}" y1="{start_point[1]:.2f}" '
        svg += f'x2="{end_point[0]:.2f}" y2="{end_point[1]:.2f}" '
        svg += f'stroke="{self.config.window_glass_stroke}" stroke-width="{self.config.window_glass_stroke_width}" />\n'

        # Two additional parallel lines for visual interest
        quarter_offset = half_depth * 0.5
        offset_x_q = quarter_offset * math.cos(perp_angle)
        offset_y_q = quarter_offset * math.sin(perp_angle)

        # Line closer to c1/c4
        svg += f'  <line x1="{start_point[0] - offset_x_q:.2f}" y1="{start_point[1] - offset_y_q:.2f}" '
        svg += f'x2="{end_point[0] - offset_x_q:.2f}" y2="{end_point[1] - offset_y_q:.2f}" '
        svg += f'stroke="{self.config.window_glass_stroke}" stroke-width="{self.config.window_glass_stroke_width}" />\n'

        # Line closer to c2/c3
        svg += f'  <line x1="{start_point[0] + offset_x_q:.2f}" y1="{start_point[1] + offset_y_q:.2f}" '
        svg += f'x2="{end_point[0] + offset_x_q:.2f}" y2="{end_point[1] + offset_y_q:.2f}" '
        svg += f'stroke="{self.config.window_glass_stroke}" stroke-width="{self.config.window_glass_stroke_width}" />\n'

        svg += '</g>'

        return svg

    def _render_constraints(self) -> str:
        """
        Render constraint lines.

        Returns:
            SVG string for constraints
        """
        # Extract unique constraints from the floorplan
        h_constraints = set()
        v_constraints = set()

        for vertex in self.floorplan.registry.get_vertices():
            for constraint in vertex.constraints:
                if isinstance(constraint, HorizontalConstraint):
                    h_constraints.add(int(constraint.get_value()))
                elif isinstance(constraint, VerticalConstraint):
                    v_constraints.add(int(constraint.get_value()))

        # Get viewbox for line dimensions
        viewbox = self._calculate_viewbox()
        width = viewbox[2]
        height = viewbox[3]

        svg = ""

        # Draw horizontal constraints
        for y_coord in sorted(h_constraints):
            svg += f'    <line x1="0" y1="{y_coord}" x2="{width}" y2="{y_coord}" '
            svg += f'stroke="{self.config.constraint_line_color}" '
            svg += f'stroke-width="{self.config.constraint_line_width}" '
            svg += f'opacity="{self.config.constraint_opacity}"/>\n'

        # Draw vertical constraints
        for x_coord in sorted(v_constraints):
            svg += f'    <line x1="{x_coord}" y1="0" x2="{x_coord}" y2="{height}" '
            svg += f'stroke="{self.config.constraint_line_color}" '
            svg += f'stroke-width="{self.config.constraint_line_width}" '
            svg += f'opacity="{self.config.constraint_opacity}"/>\n'

        return svg
