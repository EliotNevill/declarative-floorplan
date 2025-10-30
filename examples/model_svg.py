from declarative_floorplan import Floorplan, Vertex, Wall, Door, Window, Position as Pos, HorizontalConstraint as HC, VerticalConstraint as VC


# Complete representation of the model.svg floorplan with EXACT coordinates from the SVG
# This apartment layout includes ALL 13 rooms from the original model.svg

with Floorplan("Complete Apartment Floorplan - All Rooms") as fp:

    # ========== ROOM 1: OUTDOOR SPACE (ULKOTILA) - Bottom Right ==========
    # Polygon: 492.88,1325.78 492.88,1464.22 626.59,1464.22 626.59,1325.49
    od1_v1 = VC(492.88)
    od1_v2 = VC(626.59)
    od1_h1 = HC(1325.78)
    od1_h2 = HC(1464.22)

    od1_c1 = Vertex(name="Outdoor1 BL", constraints=[od1_h1, od1_v1])
    od1_c2 = Vertex(name="Outdoor1 TL", constraints=[od1_h2, od1_v1])
    od1_c3 = Vertex(name="Outdoor1 TR", constraints=[od1_h2, od1_v2])
    od1_c4 = Vertex(name="Outdoor1 BR", constraints=[HC(1325.49), od1_v2])

    od1_w1 = Wall(name="Outdoor1 Left", start_vertex=od1_c1, end_vertex=od1_c2)
    od1_w2 = Wall(name="Outdoor1 Top", start_vertex=od1_c2, end_vertex=od1_c3)
    od1_w3 = Wall(name="Outdoor1 Right", start_vertex=od1_c3, end_vertex=od1_c4)
    od1_w4 = Wall(name="Outdoor1 Bottom", start_vertex=od1_c4, end_vertex=od1_c1)

    # ========== ROOM 2: OUTDOOR SPACE (ULKOTILA) - Top ==========
    # Polygon: 48.48,265.30 48.48,45.95 594.09,45.95 594.09,264.90
    od2_v1 = VC(48.48)
    od2_v2 = VC(594.09)
    od2_h1 = HC(45.95)
    od2_h2 = HC(265.30)

    od2_c1 = Vertex(name="Outdoor2 BL", constraints=[od2_h2, od2_v1])
    od2_c2 = Vertex(name="Outdoor2 TL", constraints=[od2_h1, od2_v1])
    od2_c3 = Vertex(name="Outdoor2 TR", constraints=[od2_h1, od2_v2])
    od2_c4 = Vertex(name="Outdoor2 BR", constraints=[HC(264.90), od2_v2])

    od2_w1 = Wall(name="Outdoor2 Left", start_vertex=od2_c1, end_vertex=od2_c2)
    od2_w2 = Wall(name="Outdoor2 Top", start_vertex=od2_c2, end_vertex=od2_c3)
    od2_w3 = Wall(name="Outdoor2 Right", start_vertex=od2_c3, end_vertex=od2_c4)
    od2_w4 = Wall(name="Outdoor2 Bottom", start_vertex=od2_c4, end_vertex=od2_c1)

    # ========== ROOM 3: DINING ROOM (R) ==========
    # Polygon: 786.68,1113.48 632.78,1113.48 632.78,910.66 786.68,910.66
    dn_v1 = VC(632.78)
    dn_v2 = VC(786.68)
    dn_h1 = HC(910.66)
    dn_h2 = HC(1113.48)

    dn_c1 = Vertex(name="Dining BL", constraints=[dn_h2, dn_v2])
    dn_c2 = Vertex(name="Dining TL", constraints=[dn_h2, dn_v1])
    dn_c3 = Vertex(name="Dining TR", constraints=[dn_h1, dn_v1])
    dn_c4 = Vertex(name="Dining BR", constraints=[dn_h1, dn_v2])

    dn_w1 = Wall(name="Dining Left", start_vertex=dn_c1, end_vertex=dn_c2)
    dn_w2 = Wall(name="Dining Top", start_vertex=dn_c2, end_vertex=dn_c3)
    dn_w3 = Wall(name="Dining Right", start_vertex=dn_c3, end_vertex=dn_c4)
    dn_w4 = Wall(name="Dining Bottom", start_vertex=dn_c4, end_vertex=dn_c1)

    # ========== ROOM 4: KITCHEN (K) ==========
    # Polygon: 931.84,1310.64 632.78,1310.64 632.78,1113.48 786.68,1113.48 786.68,910.66 931.84,910.66
    kt_v1 = VC(632.78)
    kt_v2 = VC(786.68)
    kt_v3 = VC(931.84)
    kt_h1 = HC(910.66)
    kt_h2 = HC(1113.48)
    kt_h3 = HC(1310.64)

    kt_c1 = Vertex(name="Kitchen BL", constraints=[kt_h3, kt_v3])
    kt_c2 = Vertex(name="Kitchen TL", constraints=[kt_h3, kt_v1])
    kt_c3 = Vertex(name="Kitchen Mid1", constraints=[kt_h2, kt_v1])
    kt_c4 = Vertex(name="Kitchen Mid2", constraints=[kt_h2, kt_v2])
    kt_c5 = Vertex(name="Kitchen Mid3", constraints=[kt_h1, kt_v2])
    kt_c6 = Vertex(name="Kitchen BR", constraints=[kt_h1, kt_v3])

    kt_w1 = Wall(name="Kitchen Wall1", start_vertex=kt_c1, end_vertex=kt_c2)
    kt_w2 = Wall(name="Kitchen Wall2", start_vertex=kt_c2, end_vertex=kt_c3)
    kt_w3 = Wall(name="Kitchen Wall3", start_vertex=kt_c3, end_vertex=kt_c4)
    kt_w4 = Wall(name="Kitchen Wall4", start_vertex=kt_c4, end_vertex=kt_c5)
    kt_w5 = Wall(name="Kitchen Wall5", start_vertex=kt_c5, end_vertex=kt_c6)
    kt_w6 = Wall(name="Kitchen Wall6", start_vertex=kt_c6, end_vertex=kt_c1)

    # ========== ROOM 5: ENTRY/LOBBY (ET) ==========
    # Polygon: 616.78,1210.32 502.56,1210.32 414.74,1171.71 373.42,1171.71 373.42,941.50 427.29,941.50 495.90,859.10 616.78,859.10
    en_c1 = Vertex(name="Entry P1", constraints=[HC(1210.32), VC(616.78)])
    en_c2 = Vertex(name="Entry P2", constraints=[HC(1210.32), VC(502.56)])
    en_c3 = Vertex(name="Entry P3", constraints=[HC(1171.71), VC(414.74)])
    en_c4 = Vertex(name="Entry P4", constraints=[HC(1171.71), VC(373.42)])
    en_c5 = Vertex(name="Entry P5", constraints=[HC(941.50), VC(373.42)])
    en_c6 = Vertex(name="Entry P6", constraints=[HC(941.50), VC(427.29)])
    en_c7 = Vertex(name="Entry P7", constraints=[HC(859.10), VC(495.90)])
    en_c8 = Vertex(name="Entry P8", constraints=[HC(859.10), VC(616.78)])

    en_w1 = Wall(name="Entry Wall1", start_vertex=en_c1, end_vertex=en_c2)
    en_w2 = Wall(name="Entry Wall2", start_vertex=en_c2, end_vertex=en_c3)
    en_w3 = Wall(name="Entry Wall3", start_vertex=en_c3, end_vertex=en_c4)
    en_w4 = Wall(name="Entry Wall4", start_vertex=en_c4, end_vertex=en_c5)
    en_w5 = Wall(name="Entry Wall5", start_vertex=en_c5, end_vertex=en_c6)
    en_w6 = Wall(name="Entry Wall6", start_vertex=en_c6, end_vertex=en_c7)
    en_w7 = Wall(name="Entry Wall7", start_vertex=en_c7, end_vertex=en_c8)
    en_w8 = Wall(name="Entry Wall8", start_vertex=en_c8, end_vertex=en_c1)

    # ========== ROOM 6: LIVING ROOM (OH) ==========
    # Polygon: 931.84,910.66 632.78,910.66 632.78,1210.32 616.78,1210.32 616.78,859.10 495.90,859.10 495.90,280.30 931.84,280.30
    living_corner1 = Vertex(name="Living P1", constraints=[HC(910.66), VC(931.84)])
    living_corner2 = Vertex(name="Living P2", constraints=[HC(910.66), VC(632.78)])
    living_corner3 = Vertex(name="Living P3", constraints=[HC(1210.32), VC(632.78)])
    living_corner4 = Vertex(name="Living P4", constraints=[HC(1210.32), VC(616.78)])
    living_corner5 = Vertex(name="Living P5", constraints=[HC(859.10), VC(616.78)])
    living_corner6 = Vertex(name="Living P6", constraints=[HC(859.10), VC(495.90)])
    living_corner7 = Vertex(name="Living P7", constraints=[HC(280.30), VC(495.90)])
    living_corner8 = Vertex(name="Living P8", constraints=[HC(280.30), VC(931.84)])

    living_wall1 = Wall(name="Living Wall1", start_vertex=living_corner1, end_vertex=living_corner2)
    living_wall2 = Wall(name="Living Wall2", start_vertex=living_corner2, end_vertex=living_corner3)
    living_wall3 = Wall(name="Living Wall3", start_vertex=living_corner3, end_vertex=living_corner4)
    living_wall4 = Wall(name="Living Wall4", start_vertex=living_corner4, end_vertex=living_corner5)
    living_wall5 = Wall(name="Living Wall5", start_vertex=living_corner5, end_vertex=living_corner6)
    living_wall6 = Wall(name="Living Wall6", start_vertex=living_corner6, end_vertex=living_corner7)
    living_wall7 = Wall(name="Living Wall7", start_vertex=living_corner7, end_vertex=living_corner8)
    living_wall8 = Wall(name="Living Wall8", start_vertex=living_corner8, end_vertex=living_corner1)

    # ========== ROOM 7: BEDROOM 1 (MH) - Upper ==========
    # Polygon: 482.90,586.71 63.48,586.71 63.48,280.30 482.90,280.30
    bedroom1_v1 = VC(63.48)
    bedroom1_v2 = VC(482.90)
    bedroom1_h1 = HC(280.30)
    bedroom1_h2 = HC(586.71)

    bedroom1_corner1 = Vertex(name="Bedroom1 BL", constraints=[bedroom1_h2, bedroom1_v2])
    bedroom1_corner2 = Vertex(name="Bedroom1 TL", constraints=[bedroom1_h2, bedroom1_v1])
    bedroom1_corner3 = Vertex(name="Bedroom1 TR", constraints=[bedroom1_h1, bedroom1_v1])
    bedroom1_corner4 = Vertex(name="Bedroom1 BR", constraints=[bedroom1_h1, bedroom1_v2])

    bedroom1_wall1 = Wall(name="Bedroom1 Left", start_vertex=bedroom1_corner1, end_vertex=bedroom1_corner2)
    bedroom1_wall2 = Wall(name="Bedroom1 Top", start_vertex=bedroom1_corner2, end_vertex=bedroom1_corner3)
    bedroom1_wall3 = Wall(name="Bedroom1 Right", start_vertex=bedroom1_corner3, end_vertex=bedroom1_corner4)
    bedroom1_wall4 = Wall(name="Bedroom1 Bottom", start_vertex=bedroom1_corner4, end_vertex=bedroom1_corner1)

    # ========== ROOM 8: BEDROOM 2 (MH) - Lower ==========
    # Polygon: 360.42,1310.64 63.48,1310.64 63.48,941.50 360.42,941.50
    bedroom2_v1 = VC(63.48)
    bedroom2_v2 = VC(360.42)
    bedroom2_h1 = HC(941.50)
    bedroom2_h2 = HC(1310.64)

    bedroom2_corner1 = Vertex(name="Bedroom2 BL", constraints=[bedroom2_h2, bedroom2_v2])
    bedroom2_corner2 = Vertex(name="Bedroom2 TL", constraints=[bedroom2_h2, bedroom2_v1])
    bedroom2_corner3 = Vertex(name="Bedroom2 TR", constraints=[bedroom2_h1, bedroom2_v1])
    bedroom2_corner4 = Vertex(name="Bedroom2 BR", constraints=[bedroom2_h1, bedroom2_v2])

    bedroom2_wall1 = Wall(name="Bedroom2 Left", start_vertex=bedroom2_corner1, end_vertex=bedroom2_corner2)
    bedroom2_wall2 = Wall(name="Bedroom2 Top", start_vertex=bedroom2_corner2, end_vertex=bedroom2_corner3)
    bedroom2_wall3 = Wall(name="Bedroom2 Right", start_vertex=bedroom2_corner3, end_vertex=bedroom2_corner4)
    bedroom2_wall4 = Wall(name="Bedroom2 Bottom", start_vertex=bedroom2_corner4, end_vertex=bedroom2_corner1)

    # ========== ROOM 9: BATHROOM/UTILITY (KHH/PH) ==========
    # Polygon: 482.90,854.39 421.20,928.50 240.80,928.50 240.80,599.71 482.90,599.71
    bathroom_util_corner1 = Vertex(name="BathUtil P1", constraints=[HC(854.39), VC(482.90)])
    bathroom_util_corner2 = Vertex(name="BathUtil P2", constraints=[HC(928.50), VC(421.20)])
    bathroom_util_corner3 = Vertex(name="BathUtil P3", constraints=[HC(928.50), VC(240.80)])
    bathroom_util_corner4 = Vertex(name="BathUtil P4", constraints=[HC(599.71), VC(240.80)])
    bathroom_util_corner5 = Vertex(name="BathUtil P5", constraints=[HC(599.71), VC(482.90)])

    bathroom_util_wall1 = Wall(name="BathUtil Wall1", start_vertex=bathroom_util_corner1, end_vertex=bathroom_util_corner2)
    bathroom_util_wall2 = Wall(name="BathUtil Wall2", start_vertex=bathroom_util_corner2, end_vertex=bathroom_util_corner3)
    bathroom_util_wall3 = Wall(name="BathUtil Wall3", start_vertex=bathroom_util_corner3, end_vertex=bathroom_util_corner4)
    bathroom_util_wall4 = Wall(name="BathUtil Wall4", start_vertex=bathroom_util_corner4, end_vertex=bathroom_util_corner5)
    bathroom_util_wall5 = Wall(name="BathUtil Wall5", start_vertex=bathroom_util_corner5, end_vertex=bathroom_util_corner1)

    # ========== ROOM 10: UNDEFINED SPACE ==========
    # Polygon: 225.80,928.50 63.48,928.50 63.48,736.55 225.80,736.55
    undefined_v1 = VC(63.48)
    undefined_v2 = VC(225.80)
    undefined_h1 = HC(736.55)
    undefined_h2 = HC(928.50)

    undefined_corner1 = Vertex(name="Undefined BL", constraints=[undefined_h2, undefined_v2])
    undefined_corner2 = Vertex(name="Undefined TL", constraints=[undefined_h2, undefined_v1])
    undefined_corner3 = Vertex(name="Undefined TR", constraints=[undefined_h1, undefined_v1])
    undefined_corner4 = Vertex(name="Undefined BR", constraints=[undefined_h1, undefined_v2])

    undefined_wall1 = Wall(name="Undefined Left", start_vertex=undefined_corner1, end_vertex=undefined_corner2)
    undefined_wall2 = Wall(name="Undefined Top", start_vertex=undefined_corner2, end_vertex=undefined_corner3)
    undefined_wall3 = Wall(name="Undefined Right", start_vertex=undefined_corner3, end_vertex=undefined_corner4)
    undefined_wall4 = Wall(name="Undefined Bottom", start_vertex=undefined_corner4, end_vertex=undefined_corner1)

    # ========== ROOM 11: CLOSET (VH) ==========
    # Polygon: 225.80,720.55 63.48,720.55 63.48,599.71 225.80,599.71
    closet_v1 = VC(63.48)
    closet_v2 = VC(225.80)
    closet_h1 = HC(599.71)
    closet_h2 = HC(720.55)

    closet_corner1 = Vertex(name="Closet BL", constraints=[closet_h2, closet_v2])
    closet_corner2 = Vertex(name="Closet TL", constraints=[closet_h2, closet_v1])
    closet_corner3 = Vertex(name="Closet TR", constraints=[closet_h1, closet_v1])
    closet_corner4 = Vertex(name="Closet BR", constraints=[closet_h1, closet_v2])

    closet_wall1 = Wall(name="Closet Left", start_vertex=closet_corner1, end_vertex=closet_corner2)
    closet_wall2 = Wall(name="Closet Top", start_vertex=closet_corner2, end_vertex=closet_corner3)
    closet_wall3 = Wall(name="Closet Right", start_vertex=closet_corner3, end_vertex=closet_corner4)
    closet_wall4 = Wall(name="Closet Bottom", start_vertex=closet_corner4, end_vertex=closet_corner1)

    # ========== ROOM 12: BATHROOM (WC) ==========
    # Polygon: 486.56,1220.76 486.56,1310.64 373.42,1310.64 373.42,1187.71 411.38,1187.71
    wc_corner1 = Vertex(name="WC P1", constraints=[HC(1220.76), VC(486.56)])
    wc_corner2 = Vertex(name="WC P2", constraints=[HC(1310.64), VC(486.56)])
    wc_corner3 = Vertex(name="WC P3", constraints=[HC(1310.64), VC(373.42)])
    wc_corner4 = Vertex(name="WC P4", constraints=[HC(1187.71), VC(373.42)])
    wc_corner5 = Vertex(name="WC P5", constraints=[HC(1187.71), VC(411.38)])

    wc_wall1 = Wall(name="WC Wall1", start_vertex=wc_corner1, end_vertex=wc_corner2)
    wc_wall2 = Wall(name="WC Wall2", start_vertex=wc_corner2, end_vertex=wc_corner3)
    wc_wall3 = Wall(name="WC Wall3", start_vertex=wc_corner3, end_vertex=wc_corner4)
    wc_wall4 = Wall(name="WC Wall4", start_vertex=wc_corner4, end_vertex=wc_corner5)
    wc_wall5 = Wall(name="WC Wall5", start_vertex=wc_corner5, end_vertex=wc_corner1)

    # ========== ROOM 13: DRAUGHT LOBBY (TK) ==========
    # Polygon: 616.78,1310.64 502.56,1310.64 502.56,1226.32 616.78,1226.32
    tk_v1 = VC(502.56)
    tk_v2 = VC(616.78)
    tk_h1 = HC(1226.32)
    tk_h2 = HC(1310.64)

    tk_corner1 = Vertex(name="TK BL", constraints=[tk_h2, tk_v2])
    tk_corner2 = Vertex(name="TK TL", constraints=[tk_h2, tk_v1])
    tk_corner3 = Vertex(name="TK TR", constraints=[tk_h1, tk_v1])
    tk_corner4 = Vertex(name="TK BR", constraints=[tk_h1, tk_v2])

    tk_wall1 = Wall(name="TK Left", start_vertex=tk_corner1, end_vertex=tk_corner2)
    tk_wall2 = Wall(name="TK Top", start_vertex=tk_corner2, end_vertex=tk_corner3)
    tk_wall3 = Wall(name="TK Right", start_vertex=tk_corner3, end_vertex=tk_corner4)
    tk_wall4 = Wall(name="TK Bottom", start_vertex=tk_corner4, end_vertex=tk_corner1)

    # ========== WINDOWS ==========
    # Top wall windows (Outdoor2 Bottom wall, shared with Living Room)
    # From SVG: 239.80-389.84, 591.08-718.17, 724.88-843.15 (all at y=280.30/265.30)
    window_top_1 = Window(name="Top Window 1", wall=living_wall7, position=314.82, width=150.04)
    window_top_2 = Window(name="Top Window 2", wall=living_wall7, position=654.62, width=127.09)
    window_top_3 = Window(name="Top Window 3", wall=living_wall7, position=784.01, width=118.27)

    # Bottom wall windows (Bedroom2 Bottom wall and exterior)
    # From SVG: 175.45-328.09, 400.41-463.69, 722.86-873.33 (all at y=1310.64/1325.64)
    window_bottom_1 = Window(name="Bottom Window 1", wall=bedroom2_wall1, position=251.77, width=152.64)
    window_bottom_2 = Window(name="Bottom Window 2", wall=wc_wall2, position=432.05, width=63.28)
    window_bottom_3 = Window(name="Bottom Window 3", wall=kt_w6, position=798.09, width=150.47)

    # ========== DOORS ==========
    # Main entrance door to outdoor space (top wall)
    # SVG: 504.93-584.02 at y=280.30
    door_main_entrance = Door(name="Main Entrance", wall=living_wall7, position=544.47, width=79.09)

    # Door from Entry to Living Room (diagonal wall)
    # SVG: diagonal door on wall en_w6
    door_entry_living = Door(name="Entry to Living", wall=en_w6, position=Pos.CENTERED, width=75)

    # Door from Bedroom1 to Living Room (vertical wall)
    # SVG: 495.90,426.51 to 495.90,335.77 (width 90.74)
    door_bedroom1_living = Door(name="Bedroom1 to Living", wall=living_wall6, position=381.14, width=90.74)

    # Door from Bedroom1 to Bathroom/Utility area
    # SVG: 105.41-167.87 at y=599.71
    door_bedroom1_bath = Door(name="Bedroom1 to Bath", wall=bedroom1_wall4, position=136.64, width=62.46)

    # Door from Closet to Bathroom area
    # SVG: 240.80,809.03 to 240.80,743.04 (width 65.99)
    door_closet_bath = Door(name="Closet to Bath", wall=closet_wall1, position=776.03, width=65.99)

    # Door from Entry to WC (diagonal wall)
    # SVG: diagonal door on entry wall
    door_entry_wc = Door(name="Entry to WC", wall=en_w2, position=Pos.CENTERED, width=90)

    # Door from Entry/TK area to exterior (vertical wall)
    # SVG: on TK wall
    door_tk_entry = Door(name="TK to Entry", wall=en_w8, position=Pos.CENTERED, width=114.24)

    # Main exterior door (bottom outdoor space)
    # SVG: 510.90-599.54 at y=1310.64
    door_exterior_bottom = Door(name="Exterior Bottom", wall=tk_wall1, position=555.22, width=88.64)

    fp.generate_svg("examples/complete_apartment.svg")
