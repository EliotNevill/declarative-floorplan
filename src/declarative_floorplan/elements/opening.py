"""Base class for openings (doors and windows)."""

import math
from typing import Tuple, Union

from declarative_floorplan.elements.base import FloorplanElement
from declarative_floorplan.elements.wall import Wall
from declarative_floorplan.positioning.position import Position


class Opening(FloorplanElement):
    """Base class for elements that create openings in walls."""

    def __init__(
        self,
        name: str,
        wall: Wall,
        position: Union[float, Position],
        width: float,
    ) -> None:
        """
        Initialize an opening.

        Args:
            name: Human-readable name for the opening
            wall: Wall to place the opening on
            position: Position along the wall (distance from start or Position enum)
            width: Width of the opening
        """
        super().__init__(name)
        self.wall = wall
        self.position = position
        self.width = width

        # Register with active floorplan
        from declarative_floorplan.core.floorplan import Floorplan

        if Floorplan._active_floorplan is not None:
            Floorplan._active_floorplan.register_element(self)

    def get_center_position(self) -> float:
        """
        Get the center position along the wall.

        Returns:
            Distance from wall start to opening center
        """
        if isinstance(self.position, Position):
            return self.position.calculate_position(self.wall.length(), self.width)
        else:
            return self.position

    def get_center_point(self) -> Tuple[float, float]:
        """
        Get the center point of the opening in 2D space.

        Returns:
            Tuple of (x, y) coordinates
        """
        center_dist = self.get_center_position()
        return self.wall.point_at_distance(center_dist)

    def get_start_end_points(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Get the start and end points of the opening.

        Returns:
            Tuple of (start_point, end_point) coordinates
        """
        center_dist = self.get_center_position()
        half_width = self.width / 2

        start_point = self.wall.point_at_distance(center_dist - half_width)
        end_point = self.wall.point_at_distance(center_dist + half_width)

        return (start_point, end_point)

    def to_svg(self) -> str:
        """Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement to_svg()")
