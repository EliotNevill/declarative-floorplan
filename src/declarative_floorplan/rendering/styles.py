"""Style configuration for SVG rendering."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class RenderMode(Enum):
    """Rendering mode for SVG output."""

    FULL = "full"  # Render all elements (walls, doors, windows)
    CONSTRAINTS_ONLY = "constraints_only"  # Render only constraint lines


@dataclass
class ElementStyle:
    """Style configuration for a floorplan element."""

    fill: str = "#000000"
    stroke: str = "#000000"
    stroke_width: float = 1.0
    fill_opacity: float = 1.0
    stroke_opacity: float = 1.0

    def to_svg_attrs(self) -> str:
        """
        Convert style to SVG attributes string.

        Returns:
            SVG attribute string
        """
        attrs = f'fill="{self.fill}" '
        attrs += f'stroke="{self.stroke}" '
        attrs += f'stroke-width="{self.stroke_width}" '

        if self.fill_opacity != 1.0:
            attrs += f'fill-opacity="{self.fill_opacity}" '

        if self.stroke_opacity != 1.0:
            attrs += f'stroke-opacity="{self.stroke_opacity}" '

        return attrs.strip()


@dataclass
class RenderConfig:
    """Configuration for SVG rendering."""

    # Rendering mode
    render_mode: RenderMode = RenderMode.FULL

    # Wall styles
    wall_internal: ElementStyle = None
    wall_external: ElementStyle = None

    # Opening styles
    door_fill: str = "#ffffff"
    door_stroke: str = "#000000"
    door_stroke_width: float = 1.0
    door_arc_stroke: str = "#000000"
    door_arc_stroke_width: float = 1.0

    window_fill: str = "#e0e0ff"
    window_stroke: str = "#000000"
    window_stroke_width: float = 1.0
    window_glass_stroke: str = "#000000"
    window_glass_stroke_width: float = 0.5

    # Viewbox settings
    viewbox_padding: float = 20.0
    viewbox_override: Optional[Tuple[float, float, float, float]] = None

    # Constraint rendering settings
    constraint_line_color: str = "red"
    constraint_line_width: float = 2.0
    constraint_opacity: float = 0.8

    def __post_init__(self):
        """Initialize default styles if not provided."""
        if self.wall_internal is None:
            self.wall_internal = ElementStyle(
                fill="#000000",
                stroke="#000000",
                stroke_width=0.5,
            )

        if self.wall_external is None:
            self.wall_external = ElementStyle(
                fill="#000000",
                stroke="#000000",
                stroke_width=0.5,
            )

    def get_door_style(self) -> ElementStyle:
        """Get door opening style."""
        return ElementStyle(
            fill=self.door_fill,
            stroke=self.door_stroke,
            stroke_width=self.door_stroke_width,
        )

    def get_window_style(self) -> ElementStyle:
        """Get window style."""
        return ElementStyle(
            fill=self.window_fill,
            stroke=self.window_stroke,
            stroke_width=self.window_stroke_width,
        )


# Default configuration
DEFAULT_CONFIG = RenderConfig()
