"""Window element for floorplans."""

import math
from typing import Tuple, Union

from declarative_floorplan.elements.opening import Opening
from declarative_floorplan.elements.wall import Wall
from declarative_floorplan.positioning.position import Position


class Window(Opening):
    """A window opening in a wall."""

    def __init__(
        self,
        name: str,
        wall: Wall,
        position: Union[float, Position],
        width: float,
        depth: float = 5.0,
    ) -> None:
        """
        Initialize a window.

        Args:
            name: Human-readable name for the window
            wall: Wall to place the window on
            position: Position along the wall
            width: Width of the window opening
            depth: Depth of the window frame (default: 5.0)
        """
        super().__init__(name, wall, position, width)
        self.depth = depth

    def to_svg(self) -> str:
        """
        Convert window to SVG markup.

        Returns:
            SVG string representation
        """
        start_point, end_point = self.get_start_end_points()

        # Get perpendicular offsets for window depth
        wall_angle = self.wall.angle()
        perp_angle = wall_angle + math.pi / 2
        half_depth = self.depth / 2

        # Calculate four corners of window rectangle
        offset_x = half_depth * math.cos(perp_angle)
        offset_y = half_depth * math.sin(perp_angle)

        c1 = (start_point[0] - offset_x, start_point[1] - offset_y)
        c2 = (start_point[0] + offset_x, start_point[1] + offset_y)
        c3 = (end_point[0] + offset_x, end_point[1] + offset_y)
        c4 = (end_point[0] - offset_x, end_point[1] - offset_y)

        points = f"{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {c3[0]:.2f},{c3[1]:.2f} {c4[0]:.2f},{c4[1]:.2f}"

        # Create window rectangle
        svg = f'<polygon points="{points}" fill="#e0e0ff" stroke="#000000" stroke-width="1" />\n'

        # Add glass pane lines
        svg += f'<line x1="{start_point[0]:.2f}" y1="{start_point[1]:.2f}" '
        svg += f'x2="{end_point[0]:.2f}" y2="{end_point[1]:.2f}" '
        svg += 'stroke="#000000" stroke-width="0.5" />'

        return svg
