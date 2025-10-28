
from declarative_floorplan import Floorplan, Vertex, Wall, Door, Window, HorizontalConstraint, VerticalConstraint, CENTERED

with Floorplan("A basic room") as fp:
    lower_wall_horizontal_constraint = HorizontalConstraint(50)
    upper_wall_horizontal_constraint = HorizontalConstraint(100)
    left_wall_vertical_constraint = VerticalConstraint(75)
    right_wall_vertical_constraint = VerticalConstraint(125)

    lower_right_corner = Vertex(name="Lower Right Corner", constraints=[lower_wall_horizontal_constraint, right_wall_vertical_constraint])
    upper_right_corner = Vertex(name="Upper Right Corner", constraints=[upper_wall_horizontal_constraint, right_wall_vertical_constraint])
    upper_left_corner = Vertex(name="Upper Left Corner", constraints=[upper_wall_horizontal_constraint, left_wall_vertical_constraint])
    lower_left_corner = Vertex(name="Lower Left Corner", constraints=[lower_wall_horizontal_constraint, left_wall_vertical_constraint])

    lower_wall = Wall(name="Lower Wall", start_vertex=lower_left_corner, end_vertex=lower_right_corner)

    upper_wall = Wall(name="Upper Wall", start_vertex=upper_left_corner, end_vertex=upper_right_corner)

    left_wall = Wall(name="Left Wall", start_vertex=lower_left_corner, end_vertex=upper_left_corner)

    right_wall = Wall(name="Right Wall", start_vertex=lower_right_corner, end_vertex=upper_right_corner)

    door = Door(name="Main Door", wall=lower_wall, position=75, width=30)

    window = Window(name="Front Window", wall=upper_wall, position=CENTERED, width=40)

    fp.generate_svg("basic_room.svg")

