"""Position enum for semantic positioning."""

from enum import Enum


class Position(Enum):
    """Standard positions along walls."""

    CENTERED = "centered"
    START = "start"
    END = "end"

    def calculate_position(self, wall_length: float, element_width: float) -> float:
        """
        Calculate the numeric position for this semantic position.

        Args:
            wall_length: Length of the wall
            element_width: Width of the element being positioned

        Returns:
            Distance from start of wall to center of element
        """
        if self == Position.CENTERED:
            return wall_length / 2
        elif self == Position.START:
            return element_width / 2
        elif self == Position.END:
            return wall_length - element_width / 2
        else:
            raise ValueError(f"Unknown position: {self}")
