
from declarative_floorplan import Floorplan, Vertex, Wall, Door, Window, Position as Pos, HorizontalConstraint as HC, VerticalConstraint as VC
import cairosvg

fp = Floorplan("A basic room")
with fp:
    lower_wall_horizontal_constraint = HC(50)
    upper_wall_horizontal_constraint = HC(100)
    left_wall_vertical_constraint = VC(75)
    right_wall_vertical_constraint = VC(125)

    lower_right_corner = Vertex(name="Lower Right Corner", constraints=[lower_wall_horizontal_constraint, right_wall_vertical_constraint])
    upper_right_corner = Vertex(name="Upper Right Corner", constraints=[upper_wall_horizontal_constraint, right_wall_vertical_constraint])
    upper_left_corner = Vertex(name="Upper Left Corner", constraints=[upper_wall_horizontal_constraint, left_wall_vertical_constraint])
    lower_left_corner = Vertex(name="Lower Left Corner", constraints=[lower_wall_horizontal_constraint, left_wall_vertical_constraint])

    lower_wall = Wall(name="Lower Wall", start_vertex=lower_left_corner, end_vertex=lower_right_corner)

    upper_wall = Wall(name="Upper Wall", start_vertex=upper_left_corner, end_vertex=upper_right_corner)

    left_wall = Wall(name="Left Wall", start_vertex=lower_left_corner, end_vertex=upper_left_corner)

    right_wall = Wall(name="Right Wall", start_vertex=lower_right_corner, end_vertex=upper_right_corner)

    door = Door(name="Main Door", wall=lower_wall, position=Pos.CENTERED, width=30)

    window = Window(name="Front Window", wall=upper_wall, position=Pos.CENTERED, width=40)

fp.generate_svg("examples/simple_room/model.py")
cairosvg.svg2png(url="examples/simple_room/output.svg", write_to="examples/simple_room/output.png")

