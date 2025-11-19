from declarative_floorplan import (
    Floorplan, Vertex, Wall, Door, Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC
)

with Floorplan("Third Floor") as fp:
    # =========================================================
    # Step 1: Constraint Identification
    # =========================================================
    
    # Vertical Constraints (X-coordinates)
    v_outer_left = VC(40)
    v_balcony_left = VC(100)
    v_balcony_right = VC(250)
    v_rec_right = VC(290)       # Reception Right / Bed 1 Left
    v_hall_mid_left = VC(350)   # Hallway irregular shape
    v_bed_split = VC(450)       # Bed 1 Right / Bed 2 Left
    v_bed1_diag_end = VC(410)   # End of Bed 1 diagonal
    v_bed2_diag_end = VC(490)   # End of Bed 2 diagonal
    v_bath_left = VC(480)       # Bathroom left wall
    v_bath_diag_end = VC(520)   # End of Bathroom diagonal
    v_outer_right = VC(630)

    # Horizontal Constraints (Y-coordinates)
    h_balcony_top = HC(80)
    h_main_top = HC(180)
    h_bed_chamfer_start = HC(340) # Start of door diagonals for beds
    h_bed_bottom = HC(380)
    h_bath_top = HC(480)
    h_bath_diag_start = HC(520)   # Start of bath diagonal
    h_entrance_setback = HC(530)  # Hallway entrance
    h_main_bottom = HC(580)

    # =========================================================
    # Step 2: Vertex and Wall Generation
    # =========================================================

    # --- Balcony ---
    balc_tl = Vertex("Balcony TL", [h_balcony_top, v_balcony_left])
    balc_tr = Vertex("Balcony TR", [h_balcony_top, v_balcony_right])
    balc_br = Vertex("Balcony BR", [h_main_top, v_balcony_right])
    balc_bl = Vertex("Balcony BL", [h_main_top, v_balcony_left])

    Wall("Balcony Top", balc_tl, balc_tr)
    Wall("Balcony Right", balc_tr, balc_br)
    Wall("Balcony Left", balc_bl, balc_tl)
    # Bottom wall is shared with Reception, defined there

    # --- Reception Room / Kitchen ---
    rec_tl = Vertex("Rec TL", [h_main_top, v_outer_left])
    # Note: Balcony connects to this wall, but we treat the main rect as one
    rec_tr = Vertex("Rec TR", [h_main_top, v_rec_right])
    rec_br = Vertex("Rec BR", [h_main_bottom, v_rec_right])
    rec_bl = Vertex("Rec BL", [h_main_bottom, v_outer_left])

    rec_top = Wall("Rec Top", rec_tl, rec_tr)
    rec_right = Wall("Rec Right", rec_tr, rec_br)
    rec_bottom = Wall("Rec Bottom", rec_br, rec_bl)
    rec_left = Wall("Rec Left", rec_bl, rec_tl)

    # --- Bedroom 1 (Middle) ---
    # Shares rec_tr as its Top-Left
    b1_tr = Vertex("Bed1 TR", [h_main_top, v_bed_split])
    b1_br_start = Vertex("Bed1 BR Chamfer Start", [h_bed_chamfer_start, v_bed_split])
    b1_br_end = Vertex("Bed1 BR Chamfer End", [h_bed_bottom, v_bed1_diag_end])
    b1_bl = Vertex("Bed1 BL", [h_bed_bottom, v_rec_right])

    Wall("Bed1 Top", rec_tr, b1_tr)
    Wall("Bed1 Right", b1_tr, b1_br_start)
    w_bed1_door = Wall("Bed1 Door Wall", b1_br_start, b1_br_end) # Diagonal
    Wall("Bed1 Bottom", b1_br_end, b1_bl)
    # Left wall is part of rec_right, defined above, but we need the segment.
    # In this library, we usually just define the perimeter. 
    # Since rec_right spans the whole height, it covers Bed1's left side.

    # --- Bedroom 2 (Right) ---
    # Shares b1_tr as its Top-Left
    b2_tr = Vertex("Bed2 TR", [h_main_top, v_outer_right])
    b2_br = Vertex("Bed2 BR", [h_bed_bottom, v_outer_right])
    b2_bl_end = Vertex("Bed2 BL Chamfer End", [h_bed_bottom, v_bed2_diag_end])
    # Shares b1_br_start as its chamfer start point (forming the V shape)

    Wall("Bed2 Top", b1_tr, b2_tr)
    Wall("Bed2 Right", b2_tr, b2_br)
    Wall("Bed2 Bottom", b2_br, b2_bl_end)
    w_bed2_door = Wall("Bed2 Door Wall", b2_bl_end, b1_br_start) # Diagonal

    # --- Bathroom ---
    bath_tl_start = Vertex("Bath TL Chamfer Start", [h_bath_diag_start, v_bath_left])
    bath_tl_end = Vertex("Bath TL Chamfer End", [h_bath_top, v_bath_diag_end])
    bath_tr = Vertex("Bath TR", [h_bath_top, v_outer_right])
    bath_br = Vertex("Bath BR", [h_main_bottom, v_outer_right])
    bath_bl = Vertex("Bath BL", [h_main_bottom, v_bath_left])

    w_bath_door = Wall("Bath Door Wall", bath_tl_start, bath_tl_end) # Diagonal
    Wall("Bath Top", bath_tl_end, bath_tr)
    Wall("Bath Right", bath_tr, bath_br)
    Wall("Bath Bottom", bath_br, bath_bl)
    Wall("Bath Left", bath_bl, bath_tl_start)

    # --- Hallway / Entrance ---
    # The hallway is the void space, but we need to define the entrance wall at the bottom
    # Connecting Rec Right wall to Bath Left wall
    
    # We need a vertex on the Rec Right wall at the entrance height
    hall_entry_l = Vertex("Hall Entry L", [h_entrance_setback, v_rec_right])
    hall_entry_r = Vertex("Hall Entry R", [h_entrance_setback, v_bath_left]) # Connects to bath wall?
    # Looking at image, the entrance is stepped back.
    # Let's create a small entrance vestibule wall.
    
    w_entrance = Wall("Entrance", hall_entry_l, hall_entry_r)
    
    # Connecting walls to close the loop (Rec Right partially, Bath Left partially)
    # This is implicit in the shared vertices if we were building a polygon mesh,
    # but for wall objects, we have defined the bounding walls of the rooms.

    # =========================================================
    # Step 3: Adding Doors and Windows
    # =========================================================

    # -- Reception / Kitchen --
    Door("Balcony Door", wall=rec_top, position=Pos.CENTERED, width=80) # Actually a large sliding door
    Window("Rec Window", wall=rec_left, position=Pos.CENTERED, width=60)
    Window("Kitchen Window", wall=rec_bottom, position=120, width=40)
    Door("Rec Internal Door", wall=rec_right, position=400, width=35) # Leading to hall

    # -- Bedrooms --
    Window("Bed1 Window", wall=Wall("Bed1 Top Ref", rec_tr, b1_tr), position=Pos.CENTERED, width=50)
    Window("Bed2 Window", wall=Wall("Bed2 Top Ref", b1_tr, b2_tr), position=Pos.CENTERED, width=50)
    
    Door("Bed1 Door", wall=w_bed1_door, position=Pos.CENTERED, width=30)
    Door("Bed2 Door", wall=w_bed2_door, position=Pos.CENTERED, width=30)

    # -- Bathroom --
    Door("Bath Door", wall=w_bath_door, position=Pos.CENTERED, width=30)
    Window("Bath Window", wall=Wall("Bath Bottom Ref", bath_br, bath_bl), position=Pos.CENTERED, width=30)

    # -- Entrance --
    Door("Main Entrance", wall=w_entrance, position=Pos.CENTERED, width=40)