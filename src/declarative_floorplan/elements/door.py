"""Door element for floorplans."""

import math
from typing import Tuple, Union

from declarative_floorplan.elements.opening import Opening
from declarative_floorplan.elements.wall import Wall
from declarative_floorplan.positioning.position import Position


class Door(Opening):
    """A door opening in a wall."""

    def __init__(
        self,
        name: str,
        wall: Wall,
        position: Union[float, Position],
        width: float,
        swing_angle: float = 90.0,
    ) -> None:
        """
        Initialize a door.

        Args:
            name: Human-readable name for the door
            wall: Wall to place the door on
            position: Position along the wall
            width: Width of the door opening
            swing_angle: Door swing angle in degrees (default: 90)
        """
        super().__init__(name, wall, position, width)
        self.swing_angle = swing_angle

    def to_svg(self) -> str:
        """
        Convert door to SVG markup.

        Returns:
            SVG string representation
        """
        start_point, end_point = self.get_start_end_points()

        # Create the door opening (gap in wall)
        svg = f'<line x1="{start_point[0]:.2f}" y1="{start_point[1]:.2f}" '
        svg += f'x2="{end_point[0]:.2f}" y2="{end_point[1]:.2f}" '
        svg += 'stroke="#ffffff" stroke-width="1" />\n'

        # Add door swing arc
        wall_angle = self.wall.angle()
        swing_radius = self.width

        # Convert swing angle to radians
        swing_rad = math.radians(self.swing_angle)

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
        large_arc = 1 if abs(self.swing_angle) > 180 else 0

        # SVG path for arc
        svg += f'<path d="M {start_x:.2f},{start_y:.2f} '
        svg += f'A {swing_radius:.2f},{swing_radius:.2f} 0 {large_arc},1 {end_arc_x:.2f},{end_arc_y:.2f}" '
        svg += 'fill="none" stroke="#000000" stroke-width="1" />\n'

        # Add door panel line
        svg += f'<line x1="{start_x:.2f}" y1="{start_y:.2f}" '
        svg += f'x2="{end_arc_x:.2f}" y2="{end_arc_y:.2f}" '
        svg += 'stroke="#000000" stroke-width="1" />'

        return svg
