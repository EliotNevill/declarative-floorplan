"""Floorplan context manager and coordinator."""

from typing import Any, Optional

from declarative_floorplan.core.registry import ElementRegistry


class Floorplan:
    """Main coordinator and context manager for floorplan creation."""

    _active_floorplan: Optional["Floorplan"] = None

    def __init__(self, name: str, units: str = "px") -> None:
        """
        Initialize a floorplan.

        Args:
            name: Human-readable name for the floorplan
            units: Unit of measurement (default: "px")
        """
        self.name = name
        self.units = units
        self.registry = ElementRegistry()

    def __enter__(self) -> "Floorplan":
        """Enter the context manager."""
        Floorplan._active_floorplan = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        Floorplan._active_floorplan = None

    def register_element(self, element: Any) -> None:
        """
        Register an element with this floorplan.

        Args:
            element: Element to register
        """
        self.registry.register(element)

    def generate_svg(self, output_path: str) -> None:
        """
        Generate SVG output for this floorplan.

        Args:
            output_path: Path to write the SVG file
        """
        from declarative_floorplan.rendering.svg import SVGRenderer

        renderer = SVGRenderer(self)
        svg_content = renderer.render()

        with open(output_path, "w") as f:
            f.write(svg_content)

        print(f"Generated SVG: {output_path}")

    def __repr__(self) -> str:
        num_elements = len(self.registry.get_all())
        return f"Floorplan({self.name}, {num_elements} elements)"
