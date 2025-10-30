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
