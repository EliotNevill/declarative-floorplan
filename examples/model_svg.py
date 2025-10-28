
from declarative_floorplan import Floorplan, Vertex, Wall, Door, Window, HorizontalConstraint, VerticalConstraint

# Complete representation of the model.svg floorplan with EXACT coordinates from the SVG
# This apartment layout includes ALL 13 rooms from the original model.svg

with Floorplan("Complete Apartment Floorplan - All Rooms") as fp:

    # ========== ROOM 1: OUTDOOR SPACE (ULKOTILA) - Bottom Right ==========
    # Polygon: 492.88,1325.78 492.88,1464.22 626.59,1464.22 626.59,1325.49
    outdoor1_v1 = VerticalConstraint(492.88)
    outdoor1_v2 = VerticalConstraint(626.59)
    outdoor1_h1 = HorizontalConstraint(1325.78)
    outdoor1_h2 = HorizontalConstraint(1464.22)

    outdoor1_corner1 = Vertex(name="Outdoor1 BL", constraints=[outdoor1_h1, outdoor1_v1])
    outdoor1_corner2 = Vertex(name="Outdoor1 TL", constraints=[outdoor1_h2, outdoor1_v1])
    outdoor1_corner3 = Vertex(name="Outdoor1 TR", constraints=[outdoor1_h2, outdoor1_v2])
    outdoor1_corner4 = Vertex(name="Outdoor1 BR", constraints=[HorizontalConstraint(1325.49), outdoor1_v2])

    outdoor1_wall1 = Wall(name="Outdoor1 Left", start_vertex=outdoor1_corner1, end_vertex=outdoor1_corner2)
    outdoor1_wall2 = Wall(name="Outdoor1 Top", start_vertex=outdoor1_corner2, end_vertex=outdoor1_corner3)
    outdoor1_wall3 = Wall(name="Outdoor1 Right", start_vertex=outdoor1_corner3, end_vertex=outdoor1_corner4)
    outdoor1_wall4 = Wall(name="Outdoor1 Bottom", start_vertex=outdoor1_corner4, end_vertex=outdoor1_corner1)

    # ========== ROOM 2: OUTDOOR SPACE (ULKOTILA) - Top ==========
    # Polygon: 48.48,265.30 48.48,45.95 594.09,45.95 594.09,264.90
    outdoor2_v1 = VerticalConstraint(48.48)
    outdoor2_v2 = VerticalConstraint(594.09)
    outdoor2_h1 = HorizontalConstraint(45.95)
    outdoor2_h2 = HorizontalConstraint(265.30)

    outdoor2_corner1 = Vertex(name="Outdoor2 BL", constraints=[outdoor2_h2, outdoor2_v1])
    outdoor2_corner2 = Vertex(name="Outdoor2 TL", constraints=[outdoor2_h1, outdoor2_v1])
    outdoor2_corner3 = Vertex(name="Outdoor2 TR", constraints=[outdoor2_h1, outdoor2_v2])
    outdoor2_corner4 = Vertex(name="Outdoor2 BR", constraints=[HorizontalConstraint(264.90), outdoor2_v2])

    outdoor2_wall1 = Wall(name="Outdoor2 Left", start_vertex=outdoor2_corner1, end_vertex=outdoor2_corner2)
    outdoor2_wall2 = Wall(name="Outdoor2 Top", start_vertex=outdoor2_corner2, end_vertex=outdoor2_corner3)
    outdoor2_wall3 = Wall(name="Outdoor2 Right", start_vertex=outdoor2_corner3, end_vertex=outdoor2_corner4)
    outdoor2_wall4 = Wall(name="Outdoor2 Bottom", start_vertex=outdoor2_corner4, end_vertex=outdoor2_corner1)

    # ========== ROOM 3: DINING ROOM (R) ==========
    # Polygon: 786.68,1113.48 632.78,1113.48 632.78,910.66 786.68,910.66
    dining_v1 = VerticalConstraint(632.78)
    dining_v2 = VerticalConstraint(786.68)
    dining_h1 = HorizontalConstraint(910.66)
    dining_h2 = HorizontalConstraint(1113.48)

    dining_corner1 = Vertex(name="Dining BL", constraints=[dining_h2, dining_v2])
    dining_corner2 = Vertex(name="Dining TL", constraints=[dining_h2, dining_v1])
    dining_corner3 = Vertex(name="Dining TR", constraints=[dining_h1, dining_v1])
    dining_corner4 = Vertex(name="Dining BR", constraints=[dining_h1, dining_v2])

    dining_wall1 = Wall(name="Dining Left", start_vertex=dining_corner1, end_vertex=dining_corner2)
    dining_wall2 = Wall(name="Dining Top", start_vertex=dining_corner2, end_vertex=dining_corner3)
    dining_wall3 = Wall(name="Dining Right", start_vertex=dining_corner3, end_vertex=dining_corner4)
    dining_wall4 = Wall(name="Dining Bottom", start_vertex=dining_corner4, end_vertex=dining_corner1)

    # ========== ROOM 4: KITCHEN (K) ==========
    # Polygon: 931.84,1310.64 632.78,1310.64 632.78,1113.48 786.68,1113.48 786.68,910.66 931.84,910.66
    kitchen_v1 = VerticalConstraint(632.78)
    kitchen_v2 = VerticalConstraint(786.68)
    kitchen_v3 = VerticalConstraint(931.84)
    kitchen_h1 = HorizontalConstraint(910.66)
    kitchen_h2 = HorizontalConstraint(1113.48)
    kitchen_h3 = HorizontalConstraint(1310.64)

    kitchen_corner1 = Vertex(name="Kitchen BL", constraints=[kitchen_h3, kitchen_v3])
    kitchen_corner2 = Vertex(name="Kitchen TL", constraints=[kitchen_h3, kitchen_v1])
    kitchen_corner3 = Vertex(name="Kitchen Mid1", constraints=[kitchen_h2, kitchen_v1])
    kitchen_corner4 = Vertex(name="Kitchen Mid2", constraints=[kitchen_h2, kitchen_v2])
    kitchen_corner5 = Vertex(name="Kitchen Mid3", constraints=[kitchen_h1, kitchen_v2])
    kitchen_corner6 = Vertex(name="Kitchen BR", constraints=[kitchen_h1, kitchen_v3])

    kitchen_wall1 = Wall(name="Kitchen Wall1", start_vertex=kitchen_corner1, end_vertex=kitchen_corner2)
    kitchen_wall2 = Wall(name="Kitchen Wall2", start_vertex=kitchen_corner2, end_vertex=kitchen_corner3)
    kitchen_wall3 = Wall(name="Kitchen Wall3", start_vertex=kitchen_corner3, end_vertex=kitchen_corner4)
    kitchen_wall4 = Wall(name="Kitchen Wall4", start_vertex=kitchen_corner4, end_vertex=kitchen_corner5)
    kitchen_wall5 = Wall(name="Kitchen Wall5", start_vertex=kitchen_corner5, end_vertex=kitchen_corner6)
    kitchen_wall6 = Wall(name="Kitchen Wall6", start_vertex=kitchen_corner6, end_vertex=kitchen_corner1)

    # ========== ROOM 5: ENTRY/LOBBY (ET) ==========
    # Polygon: 616.78,1210.32 502.56,1210.32 414.74,1171.71 373.42,1171.71 373.42,941.50 427.29,941.50 495.90,859.10 616.78,859.10
    entry_corner1 = Vertex(name="Entry P1", constraints=[HorizontalConstraint(1210.32), VerticalConstraint(616.78)])
    entry_corner2 = Vertex(name="Entry P2", constraints=[HorizontalConstraint(1210.32), VerticalConstraint(502.56)])
    entry_corner3 = Vertex(name="Entry P3", constraints=[HorizontalConstraint(1171.71), VerticalConstraint(414.74)])
    entry_corner4 = Vertex(name="Entry P4", constraints=[HorizontalConstraint(1171.71), VerticalConstraint(373.42)])
    entry_corner5 = Vertex(name="Entry P5", constraints=[HorizontalConstraint(941.50), VerticalConstraint(373.42)])
    entry_corner6 = Vertex(name="Entry P6", constraints=[HorizontalConstraint(941.50), VerticalConstraint(427.29)])
    entry_corner7 = Vertex(name="Entry P7", constraints=[HorizontalConstraint(859.10), VerticalConstraint(495.90)])
    entry_corner8 = Vertex(name="Entry P8", constraints=[HorizontalConstraint(859.10), VerticalConstraint(616.78)])

    entry_wall1 = Wall(name="Entry Wall1", start_vertex=entry_corner1, end_vertex=entry_corner2)
    entry_wall2 = Wall(name="Entry Wall2", start_vertex=entry_corner2, end_vertex=entry_corner3)
    entry_wall3 = Wall(name="Entry Wall3", start_vertex=entry_corner3, end_vertex=entry_corner4)
    entry_wall4 = Wall(name="Entry Wall4", start_vertex=entry_corner4, end_vertex=entry_corner5)
    entry_wall5 = Wall(name="Entry Wall5", start_vertex=entry_corner5, end_vertex=entry_corner6)
    entry_wall6 = Wall(name="Entry Wall6", start_vertex=entry_corner6, end_vertex=entry_corner7)
    entry_wall7 = Wall(name="Entry Wall7", start_vertex=entry_corner7, end_vertex=entry_corner8)
    entry_wall8 = Wall(name="Entry Wall8", start_vertex=entry_corner8, end_vertex=entry_corner1)

    # ========== ROOM 6: LIVING ROOM (OH) ==========
    # Polygon: 931.84,910.66 632.78,910.66 632.78,1210.32 616.78,1210.32 616.78,859.10 495.90,859.10 495.90,280.30 931.84,280.30
    living_corner1 = Vertex(name="Living P1", constraints=[HorizontalConstraint(910.66), VerticalConstraint(931.84)])
    living_corner2 = Vertex(name="Living P2", constraints=[HorizontalConstraint(910.66), VerticalConstraint(632.78)])
    living_corner3 = Vertex(name="Living P3", constraints=[HorizontalConstraint(1210.32), VerticalConstraint(632.78)])
    living_corner4 = Vertex(name="Living P4", constraints=[HorizontalConstraint(1210.32), VerticalConstraint(616.78)])
    living_corner5 = Vertex(name="Living P5", constraints=[HorizontalConstraint(859.10), VerticalConstraint(616.78)])
    living_corner6 = Vertex(name="Living P6", constraints=[HorizontalConstraint(859.10), VerticalConstraint(495.90)])
    living_corner7 = Vertex(name="Living P7", constraints=[HorizontalConstraint(280.30), VerticalConstraint(495.90)])
    living_corner8 = Vertex(name="Living P8", constraints=[HorizontalConstraint(280.30), VerticalConstraint(931.84)])

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
    bedroom1_v1 = VerticalConstraint(63.48)
    bedroom1_v2 = VerticalConstraint(482.90)
    bedroom1_h1 = HorizontalConstraint(280.30)
    bedroom1_h2 = HorizontalConstraint(586.71)

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
    bedroom2_v1 = VerticalConstraint(63.48)
    bedroom2_v2 = VerticalConstraint(360.42)
    bedroom2_h1 = HorizontalConstraint(941.50)
    bedroom2_h2 = HorizontalConstraint(1310.64)

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
    bathroom_util_corner1 = Vertex(name="BathUtil P1", constraints=[HorizontalConstraint(854.39), VerticalConstraint(482.90)])
    bathroom_util_corner2 = Vertex(name="BathUtil P2", constraints=[HorizontalConstraint(928.50), VerticalConstraint(421.20)])
    bathroom_util_corner3 = Vertex(name="BathUtil P3", constraints=[HorizontalConstraint(928.50), VerticalConstraint(240.80)])
    bathroom_util_corner4 = Vertex(name="BathUtil P4", constraints=[HorizontalConstraint(599.71), VerticalConstraint(240.80)])
    bathroom_util_corner5 = Vertex(name="BathUtil P5", constraints=[HorizontalConstraint(599.71), VerticalConstraint(482.90)])

    bathroom_util_wall1 = Wall(name="BathUtil Wall1", start_vertex=bathroom_util_corner1, end_vertex=bathroom_util_corner2)
    bathroom_util_wall2 = Wall(name="BathUtil Wall2", start_vertex=bathroom_util_corner2, end_vertex=bathroom_util_corner3)
    bathroom_util_wall3 = Wall(name="BathUtil Wall3", start_vertex=bathroom_util_corner3, end_vertex=bathroom_util_corner4)
    bathroom_util_wall4 = Wall(name="BathUtil Wall4", start_vertex=bathroom_util_corner4, end_vertex=bathroom_util_corner5)
    bathroom_util_wall5 = Wall(name="BathUtil Wall5", start_vertex=bathroom_util_corner5, end_vertex=bathroom_util_corner1)

    # ========== ROOM 10: UNDEFINED SPACE ==========
    # Polygon: 225.80,928.50 63.48,928.50 63.48,736.55 225.80,736.55
    undefined_v1 = VerticalConstraint(63.48)
    undefined_v2 = VerticalConstraint(225.80)
    undefined_h1 = HorizontalConstraint(736.55)
    undefined_h2 = HorizontalConstraint(928.50)

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
    closet_v1 = VerticalConstraint(63.48)
    closet_v2 = VerticalConstraint(225.80)
    closet_h1 = HorizontalConstraint(599.71)
    closet_h2 = HorizontalConstraint(720.55)

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
    wc_corner1 = Vertex(name="WC P1", constraints=[HorizontalConstraint(1220.76), VerticalConstraint(486.56)])
    wc_corner2 = Vertex(name="WC P2", constraints=[HorizontalConstraint(1310.64), VerticalConstraint(486.56)])
    wc_corner3 = Vertex(name="WC P3", constraints=[HorizontalConstraint(1310.64), VerticalConstraint(373.42)])
    wc_corner4 = Vertex(name="WC P4", constraints=[HorizontalConstraint(1187.71), VerticalConstraint(373.42)])
    wc_corner5 = Vertex(name="WC P5", constraints=[HorizontalConstraint(1187.71), VerticalConstraint(411.38)])

    wc_wall1 = Wall(name="WC Wall1", start_vertex=wc_corner1, end_vertex=wc_corner2)
    wc_wall2 = Wall(name="WC Wall2", start_vertex=wc_corner2, end_vertex=wc_corner3)
    wc_wall3 = Wall(name="WC Wall3", start_vertex=wc_corner3, end_vertex=wc_corner4)
    wc_wall4 = Wall(name="WC Wall4", start_vertex=wc_corner4, end_vertex=wc_corner5)
    wc_wall5 = Wall(name="WC Wall5", start_vertex=wc_corner5, end_vertex=wc_corner1)

    # ========== ROOM 13: DRAUGHT LOBBY (TK) ==========
    # Polygon: 616.78,1310.64 502.56,1310.64 502.56,1226.32 616.78,1226.32
    tk_v1 = VerticalConstraint(502.56)
    tk_v2 = VerticalConstraint(616.78)
    tk_h1 = HorizontalConstraint(1226.32)
    tk_h2 = HorizontalConstraint(1310.64)

    tk_corner1 = Vertex(name="TK BL", constraints=[tk_h2, tk_v2])
    tk_corner2 = Vertex(name="TK TL", constraints=[tk_h2, tk_v1])
    tk_corner3 = Vertex(name="TK TR", constraints=[tk_h1, tk_v1])
    tk_corner4 = Vertex(name="TK BR", constraints=[tk_h1, tk_v2])

    tk_wall1 = Wall(name="TK Left", start_vertex=tk_corner1, end_vertex=tk_corner2)
    tk_wall2 = Wall(name="TK Top", start_vertex=tk_corner2, end_vertex=tk_corner3)
    tk_wall3 = Wall(name="TK Right", start_vertex=tk_corner3, end_vertex=tk_corner4)
    tk_wall4 = Wall(name="TK Bottom", start_vertex=tk_corner4, end_vertex=tk_corner1)

    fp.generate_svg("complete_apartment.svg")
