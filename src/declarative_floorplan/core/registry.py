"""Element registry for tracking floorplan components."""

from typing import Any, Dict, List, Type


class ElementRegistry:
    """Registry for tracking all elements in a floorplan."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._elements: List[Any] = []
        self._by_type: Dict[str, List[Any]] = {}

    def register(self, element: Any) -> None:
        """
        Register an element.

        Args:
            element: Element to register
        """
        self._elements.append(element)

        # Track by type
        type_name = element.__class__.__name__
        if type_name not in self._by_type:
            self._by_type[type_name] = []
        self._by_type[type_name].append(element)

    def get_all(self) -> List[Any]:
        """
        Get all registered elements.

        Returns:
            List of all elements
        """
        return self._elements.copy()

    def get_by_type(self, element_type: Type) -> List[Any]:
        """
        Get elements of a specific type.

        Args:
            element_type: Type to filter by

        Returns:
            List of elements of the specified type
        """
        type_name = element_type.__name__
        return self._by_type.get(type_name, []).copy()

    def get_vertices(self) -> List[Any]:
        """Get all vertices."""
        from declarative_floorplan.geometry.vertex import Vertex

        return self.get_by_type(Vertex)

    def get_walls(self) -> List[Any]:
        """Get all walls."""
        from declarative_floorplan.elements.wall import Wall

        return self.get_by_type(Wall)

    def get_doors(self) -> List[Any]:
        """Get all doors."""
        from declarative_floorplan.elements.door import Door

        return self.get_by_type(Door)

    def get_windows(self) -> List[Any]:
        """Get all windows."""
        from declarative_floorplan.elements.window import Window

        return self.get_by_type(Window)

    def get_constraints(self) -> List[Any]:
        """Get all constraints (HC and VC)."""
        from declarative_floorplan.geometry.constraints import (
            HorizontalConstraint,
            VerticalConstraint,
        )

        # Get both HC and VC constraints
        h_constraints = self.get_by_type(HorizontalConstraint)
        v_constraints = self.get_by_type(VerticalConstraint)
        return h_constraints + v_constraints

    def clear(self) -> None:
        """Clear all registered elements."""
        self._elements.clear()
        self._by_type.clear()
