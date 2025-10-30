"""Base class for all floorplan elements."""

from abc import ABC, abstractmethod


class FloorplanElement(ABC):
    """Abstract base class for all floorplan elements."""

    def __init__(self, name: str) -> None:
        """
        Initialize a floorplan element.

        Args:
            name: Human-readable name for the element
        """
        self.name = name

    @abstractmethod
    def to_svg(self) -> str:
        """
        Convert this element to SVG markup.

        Returns:
            SVG string representation
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
