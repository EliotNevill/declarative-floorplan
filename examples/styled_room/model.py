"""Example demonstrating custom styling with RenderConfig."""

from declarative_floorplan import (
    Floorplan,
    Vertex,
    Wall,
    Door,
    Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC,
    RenderConfig,
    ElementStyle,
)

# Create a custom render configuration
custom_config = RenderConfig(
    # Walls with blue fill and thicker stroke
    wall_internal=ElementStyle(
        fill="#1a1a3e",
        stroke="#0f0f23",
        stroke_width=1.5,
    ),
    # Red door styling
    door_fill="#ffffff",
    door_stroke="#cc0000",
    door_stroke_width=2.0,
    door_arc_stroke="#990000",
    door_arc_stroke_width=1.5,
    # Green-tinted windows
    window_fill="#c0ffc0",
    window_stroke="#00aa00",
    window_stroke_width=1.5,
    window_glass_stroke="#006600",
    window_glass_stroke_width=1.0,
    # More padding around the viewbox
    viewbox_padding=30.0,
)

with Floorplan("Styled Room Example") as fp:
    # Create a simple rectangular room
    h1 = HC(50)
    h2 = HC(100)
    v1 = VC(75)
    v2 = VC(125)

    bl = Vertex(name="Bottom Left", constraints=[h1, v1])
    br = Vertex(name="Bottom Right", constraints=[h1, v2])
    tr = Vertex(name="Top Right", constraints=[h2, v2])
    tl = Vertex(name="Top Left", constraints=[h2, v1])

    Wall(name="Bottom", start_vertex=bl, end_vertex=br)
    Wall(name="Right", start_vertex=br, end_vertex=tr)
    Wall(name="Top", start_vertex=tr, end_vertex=tl)
    left_wall = Wall(name="Left", start_vertex=tl, end_vertex=bl)

    # Add a door and window
    Door(name="Entry", wall=left_wall, position=Pos.CENTERED, width=25)
    Window(name="View", wall=Wall(name="Top", start_vertex=tl, end_vertex=tr), position=Pos.CENTERED, width=35)

    # Generate with custom styling
    fp.generate_svg("examples/styled_room/output.svg", config=custom_config)

print("Compare styled_room/output.svg with basic_room.svg to see the styling differences!")
