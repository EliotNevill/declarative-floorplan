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
