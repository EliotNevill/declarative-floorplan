"""Constraint classes for vertex positioning."""

from abc import abstractmethod

from declarative_floorplan.elements.base import FloorplanElement


class Constraint(FloorplanElement):
    """Abstract base class for positioning constraints."""

    @abstractmethod
    def get_value(self) -> float:
        """Return the constraint value."""
        pass

    @abstractmethod
    def get_axis(self) -> str:
        """Return 'x' or 'y' to indicate which axis this constrains."""
        pass


class HorizontalConstraint(Constraint):
    """Constraint that fixes the Y coordinate (horizontal line)."""

    def __init__(self, value: float, name: str = None) -> None:
        """
        Initialize a horizontal constraint.

        Args:
            value: The Y coordinate value
            name: Optional name (defaults to "HC({value})")
        """
        self.value = value
        # Call parent __init__ which handles registration
        super().__init__(name or f"HC({value})")

    def get_value(self) -> float:
        """Return the Y coordinate."""
        return self.value

    def get_axis(self) -> str:
        """Return 'y' since this constrains the Y axis."""
        return "y"

    def __repr__(self) -> str:
        return f"HC({self.value})"


class VerticalConstraint(Constraint):
    """Constraint that fixes the X coordinate (vertical line)."""

    def __init__(self, value: float, name: str = None) -> None:
        """
        Initialize a vertical constraint.

        Args:
            value: The X coordinate value
            name: Optional name (defaults to "VC({value})")
        """
        self.value = value
        # Call parent __init__ which handles registration
        super().__init__(name or f"VC({value})")

    def get_value(self) -> float:
        """Return the X coordinate."""
        return self.value

    def get_axis(self) -> str:
        """Return 'x' since this constrains the X axis."""
        return "x"

    def __repr__(self) -> str:
        return f"VC({self.value})"
