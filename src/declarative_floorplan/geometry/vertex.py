"""Vertex class for floorplan points."""

from typing import List, Optional, Tuple

from declarative_floorplan.geometry.constraints import Constraint


class Vertex:
    """A point in 2D space defined by constraints."""

    def __init__(self, name: str, constraints: List[Constraint]) -> None:
        """
        Initialize a vertex.

        Args:
            name: Human-readable name for the vertex
            constraints: List of constraints (should include HC and VC)
        """
        self.name = name
        self.constraints = constraints
        self._position: Optional[Tuple[float, float]] = None

        # Register with active floorplan if in context
        from declarative_floorplan.core.floorplan import Floorplan

        if Floorplan._active_floorplan is not None:
            Floorplan._active_floorplan.register_element(self)

    def get_position(self) -> Tuple[float, float]:
        """
        Get the resolved position of this vertex.

        Returns:
            Tuple of (x, y) coordinates
        """
        if self._position is None:
            self._position = self._solve_position()
        return self._position

    def _solve_position(self) -> Tuple[float, float]:
        """
        Solve the constraints to determine position.

        Returns:
            Tuple of (x, y) coordinates
        """
        x: Optional[float] = None
        y: Optional[float] = None

        for constraint in self.constraints:
            axis = constraint.get_axis()
            value = constraint.get_value()

            if axis == "x":
                if x is not None:
                    raise ValueError(
                        f"Vertex {self.name} has multiple X constraints"
                    )
                x = value
            elif axis == "y":
                if y is not None:
                    raise ValueError(
                        f"Vertex {self.name} has multiple Y constraints"
                    )
                y = value

        if x is None or y is None:
            raise ValueError(
                f"Vertex {self.name} must have both X and Y constraints"
            )

        return (x, y)

    def __repr__(self) -> str:
        try:
            pos = self.get_position()
            return f"Vertex({self.name}, pos={pos})"
        except:
            return f"Vertex({self.name}, unresolved)"
