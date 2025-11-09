# Re-creating the given apartment plan with declarative-floorplan
# The origin (0,0) is at the top-left of the canvas.
# Units are arbitrary; proportions are chosen to match the image.

from declarative_floorplan import (
    Floorplan, Vertex, Wall, Door, Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC,
)

with Floorplan("Third Floor – 2BR with Balcony") as fp:
    # ------------------------------------------------------------
    # Step 1 — Global positioning constraints (the "planes")
    # ------------------------------------------------------------
    # Horizontal guide lines (y)
    h_0   = HC(0)     # top exterior
    h_420 = HC(420)   # line under the two bedrooms (top of corridor/bath)
    h_700 = HC(700)   # bottom exterior

    # Vertical guide lines (x)
    v_0    = VC(0)     # left exterior
    v_560  = VC(560)   # reception ↔ middle bedroom
    v_780  = VC(780)   # middle bedroom ↔ right bedroom / corridor edge
    v_900  = VC(900)   # corridor ↔ bathroom
    v_1000 = VC(1000)  # right exterior

    # ------------------------------------------------------------
    # Step 2 — Vertices and walls (room by room)
    # ------------------------------------------------------------
    # Outer rectangle corners
    tl = Vertex("Exterior TL", constraints=[h_0,   v_0])
    tr = Vertex("Exterior TR", constraints=[h_0,   v_1000])
    br = Vertex("Exterior BR", constraints=[h_700, v_1000])
    bl = Vertex("Exterior BL", constraints=[h_700, v_0])

    # Inner grid intersections
    t_v560 = Vertex("Top v560", constraints=[h_0,   v_560])
    t_v780 = Vertex("Top v780", constraints=[h_0,   v_780])

    c560_420 = Vertex("v560@h420", constraints=[h_420, v_560])
    c780_420 = Vertex("v780@h420", constraints=[h_420, v_780])
    c900_420 = Vertex("v900@h420", constraints=[h_420, v_900])
    c1000_420 = Vertex("v1000@h420", constraints=[h_420, v_1000])

    b_v560 = Vertex("Bottom v560", constraints=[h_700, v_560])
    b_v780 = Vertex("Bottom v780", constraints=[h_700, v_780])
    b_v900 = Vertex("Bottom v900", constraints=[h_700, v_900])

    # --- Exterior walls
    w_left   = Wall("Exterior Left",   start_vertex=tl, end_vertex=bl)
    w_bottom = Wall("Exterior Bottom", start_vertex=bl, end_vertex=br)
    w_right  = Wall("Exterior Right",  start_vertex=br, end_vertex=tr)
    w_top    = Wall("Exterior Top",    start_vertex=tr, end_vertex=tl)

    # --- Internal partitions
    # Reception ↔ Bedrooms divider
    w_v560_full = Wall("v560 (Reception/MidBed)", start_vertex=t_v560, end_vertex=b_v560)
    # Mid bed ↔ Right bed / corridor divider
    w_v780_full = Wall("v780 (MidBed/RightSide)", start_vertex=t_v780, end_vertex=b_v780)
    # Top-of-corridor line (under both bedrooms, across to exterior right)
    w_h420 = Wall("h420 (Top of Corridor/Bath)", start_vertex=c560_420, end_vertex=c1000_420)
    # Corridor ↔ Bathroom divider
    w_v900 = Wall("v900 (Corridor/Bath)", start_vertex=c900_420, end_vertex=b_v900)

    # ------------------------------------------------------------
    # Step 3 — Openings (doors & windows)
    # ------------------------------------------------------------
    # Entry door from exterior into corridor (bottom wall, roughly centered)
    Door("Entry Door", wall=w_bottom, position=650, width=90)

    # Door from corridor to Middle Bedroom (on h420 between v560 and v780)
    Door("Door to Middle Bedroom", wall=w_h420, position=Pos.CENTERED, width=80)

    # Door from corridor to Right Bedroom (on v780 between h420 and bottom)
    Door("Door to Right Bedroom", wall=w_v780_full, position=520, width=80)  # measured from top of that wall

    # Door from corridor to Bathroom (on v900 between h420 and bottom)
    Door("Bathroom Door", wall=w_v900, position=Pos.CENTERED, width=80)

    # Balcony doors (large opening on top wall over the Reception Room)
    Door("Balcony Doors", wall=w_top, position=160, width=180)

    # Windows along the top wall above the two bedrooms
    Window("Mid Bedroom Window", wall=w_top, position=650, width=90)
    Window("Right Bedroom Window", wall=w_top, position=880, width=90)
