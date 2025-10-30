"""Wall element for floorplans."""

import math
from typing import Tuple

from declarative_floorplan.elements.base import FloorplanElement
from declarative_floorplan.geometry.vertex import Vertex


class Wall(FloorplanElement):
    """A wall connecting two vertices."""

    def __init__(
        self, name: str, start_vertex: Vertex, end_vertex: Vertex, thickness: float = 15.0
    ) -> None:
        """
        Initialize a wall.

        Args:
            name: Human-readable name for the wall
            start_vertex: Starting vertex
            end_vertex: Ending vertex
            thickness: Wall thickness in pixels (default: 15.0)
        """
        super().__init__(name)
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.thickness = thickness

        # Register with active floorplan
        from declarative_floorplan.core.floorplan import Floorplan

        if Floorplan._active_floorplan is not None:
            Floorplan._active_floorplan.register_element(self)

    def length(self) -> float:
        """
        Calculate the length of the wall.

        Returns:
            Wall length
        """
        p1 = self.start_vertex.get_position()
        p2 = self.end_vertex.get_position()
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def angle(self) -> float:
        """
        Calculate the angle of the wall in radians.

        Returns:
            Angle in radians from start to end vertex
        """
        p1 = self.start_vertex.get_position()
        p2 = self.end_vertex.get_position()
        return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

    def midpoint(self) -> Tuple[float, float]:
        """
        Calculate the midpoint of the wall.

        Returns:
            Tuple of (x, y) coordinates
        """
        p1 = self.start_vertex.get_position()
        p2 = self.end_vertex.get_position()
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def point_at_distance(self, distance: float) -> Tuple[float, float]:
        """
        Get a point at a specific distance from the start vertex.

        Args:
            distance: Distance from start vertex

        Returns:
            Tuple of (x, y) coordinates
        """
        p1 = self.start_vertex.get_position()
        p2 = self.end_vertex.get_position()
        length = self.length()

        if length == 0:
            return p1

        ratio = distance / length
        x = p1[0] + ratio * (p2[0] - p1[0])
        y = p1[1] + ratio * (p2[1] - p1[1])
        return (x, y)

    def get_perpendicular_offset(
        self, point: Tuple[float, float], offset: float
    ) -> Tuple[float, float]:
        """
        Get a point offset perpendicular to the wall.

        Args:
            point: Point on the wall
            offset: Distance to offset (positive = left, negative = right)

        Returns:
            Offset point coordinates
        """
        angle = self.angle()
        perp_angle = angle + math.pi / 2
        x = point[0] + offset * math.cos(perp_angle)
        y = point[1] + offset * math.sin(perp_angle)
        return (x, y)

    def __repr__(self) -> str:
        return f"Wall({self.name}, {self.start_vertex.name} -> {self.end_vertex.name})"
