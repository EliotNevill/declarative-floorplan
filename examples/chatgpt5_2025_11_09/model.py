from declarative_floorplan import (
    Floorplan, Vertex, Wall, Door, Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC
)

with Floorplan("Third Floor") as fp:
    # ---------------------------------------------
    # Step 1 — Corrected Constraint Identification
    # ---------------------------------------------

    # Horizontal (Y) constraints
    h_150 = HC(150)   # balcony top rail
    h_200 = HC(200)   # balcony bottom / external top
    h_340 = HC(340)   # reception ceiling / bedroom 1 top
    h_445 = HC(445)   # hallway top (doors)
    h_555 = HC(555)   # bathroom top
    h_760 = HC(760)   # bottom external wall

    # Vertical (X) constraints
    v_25  = VC(25)    # left external wall
    v_245 = VC(245)   # reception → bedroom1 wall
    v_325 = VC(325)   # bedroom1 left wall
    v_450 = VC(450)   # bedroom1 → bedroom2 wall
    v_515 = VC(515)   # bathroom left wall
    v_640 = VC(640)   # right external wall
