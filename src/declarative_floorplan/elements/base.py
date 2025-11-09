"""Base class for all floorplan elements."""

from abc import ABC


class FloorplanElement(ABC):
    """Abstract base class for all floorplan elements."""

    def __init__(self, name: str) -> None:
        """
        Initialize a floorplan element.

        Args:
            name: Human-readable name for the element
        """
        self.name = name

        # Register with active floorplan if in context
        from declarative_floorplan.core.floorplan import Floorplan

        if Floorplan._active_floorplan is not None:
            Floorplan._active_floorplan.register_element(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
