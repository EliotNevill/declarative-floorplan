import sys
from declarative_floorplan import (
    Floorplan,
    Vertex,
    Wall,
    Door,
    Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC,
)

# Set a high recursion depth for complex floorplans
sys.setrecursionlimit(5000)

with Floorplan("Sample Floorplan") as fp:
    """
    Step 1: Constraint Identification
    Define all unique horizontal (y-axis) and vertical (x-axis)
    lines that define wall alignments.
    """
    # Horizontal Constraints (Y-axis)
    h_0 = HC(0)    # Top outer wall
    h_1 = HC(300)  # Bottom of Top MH / Top of KHH/VH
    h_2 = HC(370)  # Bottom of VH / Top of Stairs (ND)
    h_3 = HC(550)  # Bottom of KHH/Stairs / Top of ET & Bottom MH
    h_4 = HC(700)  # Bottom of Bottom MH & ET / Top of WC & TK
    h_5 = HC(800)  # Bottom outer wall

    # Vertical Constraints (X-axis)
    v_0 = VC(0)    # Left outer wall
    v_1 = VC(150)  # Left wall of VH
    v_2 = VC(250)  # Right wall of VH / Left of Stairs (ND)
    v_3 = VC(350)  # Right of Top MH & Stairs / Left of OH & KHH
    v_4 = VC(450)  # Right of Bottom MH / Left of ET & WC
    v_5 = VC(550)  # Right of WC / Left of TK
    v_6 = VC(650)  # Right of KHH/ET/TK / Left of OH/R/K
    v_7 = VC(1000) # Right outer wall

    """
    Step 2: Vertex and Wall Generation (Room by Room)
    Define vertices at the intersections of constraints and
    connect them with walls, reusing vertices for shared corners.
    """

    ## -----------------
    ## Room: Top MH (MH)
    ## -----------------
    v_mh1_tl = Vertex("MH1 TL", constraints=[h_0, v_0])
    v_mh1_tr = Vertex("MH1 TR", constraints=[h_0, v_3])
    v_mh1_br = Vertex("MH1 BR", constraints=[h_1, v_3])
    v_mh1_mid = Vertex("MH1 Mid-Bottom", constraints=[h_1, v_1])
    v_mh1_bl = Vertex("MH1 BL", constraints=[h_1, v_0])

    w_mh1_top = Wall("MH1 Top", v_mh1_tl, v_mh1_tr)
    w_mh1_right = Wall("MH1 Right", v_mh1_tr, v_mh1_br)
    w_mh1_bottom_1 = Wall("MH1 Bottom (Right)", v_mh1_br, v_mh1_mid)
    w_mh1_bottom_2 = Wall("MH1 Bottom (Left)", v_mh1_mid, v_mh1_bl)
    w_mh1_left = Wall("MH1 Left", v_mh1_bl, v_mh1_tl)

    ## -----------------
    ## Room: VH (Wardrobe)
    ## -----------------
    v_vh_tl = v_mh1_mid  # Reused
    v_vh_tr = Vertex("VH TR", constraints=[h_1, v_2])
    v_vh_br = Vertex("VH BR", constraints=[h_2, v_2])
    v_vh_bl = Vertex("VH BL", constraints=[h_2, v_1])

    w_vh_top = Wall("VH Top", v_vh_tl, v_vh_tr)
    w_vh_right = Wall("VH Right", v_vh_tr, v_vh_br)
    w_vh_bottom = Wall("VH Bottom", v_vh_br, v_vh_bl)
    w_vh_left = Wall("VH Left", v_vh_bl, v_vh_tl)

    ## -----------------
    ## Room: Stairs (ND)
    ## -----------------
    v_nd_tl = v_vh_br  # Reused
    v_nd_tr = Vertex("ND TR", constraints=[h_2, v_3])
    v_nd_br = Vertex("ND BR", constraints=[h_3, v_3])
    v_nd_bl = Vertex("ND BL", constraints=[h_3, v_2])

    w_nd_top = Wall("ND Top", v_nd_tl, v_nd_tr)
    w_nd_right = Wall("ND Right", v_nd_tr, v_nd_br)
    w_nd_bottom = Wall("ND Bottom", v_nd_br, v_nd_bl)
    w_nd_left = Wall("ND Left", v_nd_bl, v_nd_tl)

    ## -----------------
    ## Room: KHH/PH (Utility/Bath)
    ## -----------------
    v_khh_tl = v_mh1_br  # Reused
    v_khh_tr = Vertex("KHH TR", constraints=[h_1, v_6])
    v_khh_br = Vertex("KHH BR", constraints=[h_3, v_6])
    v_khh_bl = v_nd_br  # Reused

    w_khh_top = Wall("KHH Top", v_khh_tl, v_khh_tr)
    w_khh_right = Wall("KHH Right", v_khh_tr, v_khh_br)
    w_khh_bottom = Wall("KHH Bottom", v_khh_br, v_khh_bl)
    # This wall is composed of shared segments
    w_khh_left = Wall("KHH Left", v_khh_bl, v_khh_tl)

    ## -----------------
    ## Room: Bottom MH (MH)
    ## -----------------
    v_mh2_tl = Vertex("MH2 TL", constraints=[h_3, v_0])
    v_mh2_tr = Vertex("MH2 TR", constraints=[h_3, v_4])
    v_mh2_br = Vertex("MH2 BR", constraints=[h_4, v_4])
    v_mh2_bl = Vertex("MH2 BL", constraints=[h_4, v_0])

    w_mh2_top = Wall("MH2 Top", v_mh2_tl, v_mh2_tr)
    w_mh2_right = Wall("MH2 Right", v_mh2_tr, v_mh2_br)
    w_mh2_bottom = Wall("MH2 Bottom", v_mh2_br, v_mh2_bl)
    w_mh2_left = Wall("MH2 Left", v_mh2_bl, v_mh2_tl)

    ## -----------------
    ## Room: ET (Entrance Hall)
    ## -----------------
    v_et_tl = v_mh2_tr  # Reused
    v_et_tr = v_khh_br  # Reused
    v_et_br = Vertex("ET BR", constraints=[h_4, v_6])
    v_et_mid_bottom = Vertex("ET Mid-Bottom", constraints=[h_4, v_5])
    v_et_bl = v_mh2_br  # Reused

    w_et_top = Wall("ET Top", v_et_tl, v_et_tr)  # Shared w_khh_bottom
    w_et_right = Wall("ET Right", v_et_tr, v_et_br)
    w_et_bottom_1 = Wall("ET Bottom (Right)", v_et_br, v_et_mid_bottom)
    w_et_bottom_2 = Wall("ET Bottom (Left)", v_et_mid_bottom, v_et_bl)
    w_et_left = Wall("ET Left", v_et_bl, v_et_tl)  # Shared w_mh2_right

    ## -----------------
    ## Room: WC
    ## -----------------
    v_wc_tl = v_et_bl  # Reused
    v_wc_tr = v_et_mid_bottom  # Reused
    v_wc_br = Vertex("WC BR", constraints=[h_5, v_5])
    v_wc_bl = Vertex("WC BL", constraints=[h_5, v_4])

    w_wc_top = Wall("WC Top", v_wc_tl, v_wc_tr)  # Shared w_et_bottom_2
    w_wc_right = Wall("WC Right", v_wc_tr, v_wc_br)
    w_wc_bottom = Wall("WC Bottom", v_wc_br, v_wc_bl)
    w_wc_left = Wall("WC Left", v_wc_bl, v_wc_tl)

    ## -----------------
    ## Room: TK (Technical Room)
    ## -----------------
    v_tk_tl = v_wc_tr  # Reused
    v_tk_tr = v_et_br  # Reused
    v_tk_br = Vertex("TK BR", constraints=[h_5, v_6])
    v_tk_bl = v_wc_br  # Reused

    w_tk_top = Wall("TK Top", v_tk_tl, v_tk_tr)  # Shared w_et_bottom_1
    w_tk_right = Wall("TK Right", v_tk_tr, v_tk_br)
    w_tk_bottom = Wall("TK Bottom", v_tk_br, v_tk_bl)
    w_tk_left = Wall("TK Left", v_tk_bl, v_tk_tl)  # Shared w_wc_right

    ## -----------------
    ## Room: Living Area (OH, R, K)
    ## -----------------
    v_liv_tl = v_mh1_tr  # Reused
    v_liv_tr = Vertex("LIV TR", constraints=[h_0, v_7])
    v_liv_br = Vertex("LIV BR", constraints=[h_5, v_7])
    v_liv_bl_1 = v_tk_br  # Reused
    v_liv_bl_2 = v_tk_tr  # Reused
    v_liv_bl_3 = v_khh_br # Reused
    v_liv_bl_4 = v_khh_tr # Reused
    v_liv_bl_5 = v_mh1_br # Reused

    w_liv_top = Wall("LIV Top", v_liv_tl, v_liv_tr)
    w_liv_right = Wall("LIV Right", v_liv_tr, v_liv_br)
    w_liv_bottom = Wall("LIV Bottom", v_liv_br, v_liv_bl_1)
    # The left wall is a combination of other rooms' outer walls
    w_liv_left_1 = Wall("LIV Left (by TK)", v_liv_bl_1, v_liv_bl_2) # Shared w_tk_right
    w_liv_left_2 = Wall("LIV Left (by ET)", v_liv_bl_2, v_liv_bl_3) # Shared w_et_right
    w_liv_left_3 = Wall("LIV Left (by KHH)", v_liv_bl_3, v_liv_bl_4) # Shared w_khh_right
    w_liv_left_4 = Wall("LIV Left (by KHH Top)", v_liv_bl_4, v_liv_bl_5) # Shared w_khh_top
    w_liv_left_5 = Wall("LIV Left (by MH1)", v_liv_bl_5, v_liv_tl) # Shared w_mh1_right

    """
    Step 3: Adding Doors and Windows
    Place openings on their corresponding walls.
    """

    # Top MH
    Window("w_mh1_top", wall=w_mh1_top, width=120, position=Pos.CENTERED)
    Window("w_mh1_left", wall=w_mh1_left, width=120, position=Pos.CENTERED)
    Door("d_mh1", wall=w_mh1_right, width=90, position=150)

    # VH
    Door("d_vh", wall=w_vh_bottom, width=80, position=Pos.CENTERED)

    # KHH/PH
    Door("d_khh", wall=w_khh_bottom, width=90, position=100)

    # Bottom MH
    Window("w_mh2_left", wall=w_mh2_left, width=120, position=Pos.CENTERED)
    Door("d_mh2", wall=w_mh2_right, width=90, position=Pos.CENTERED)

    # ET
    Door("d_et_wc", wall=w_et_bottom_2, width=90, position=Pos.CENTERED)
    Door("d_et_tk", wall=w_et_bottom_1, width=90, position=Pos.CENTERED)

    # WC
    Window("w_wc_bottom", wall=w_wc_bottom, width=60, position=Pos.CENTERED)

    # TK (Main Entrance)
    Door("d_main_entry", wall=w_tk_bottom, width=100, position=Pos.CENTERED)

    # Living Area (OH, R, K)
    Door("d_patio_top", wall=w_liv_top, width=120, position=100)
    Window("w_liv_top", wall=w_liv_top, width=200, position=300)
    Window("w_liv_right_1", wall=w_liv_right, width=150, position=200)
    Window("w_liv_right_2", wall=w_liv_right, width=150, position=500)
    Window("w_liv_bottom", wall=w_liv_bottom, width=200, position=Pos.CENTERED)

    # --- Generate the floorplan ---
    fp.generate_svg("examples/gemeni_pro_2025_11_03/output.svg")