from declarative_floorplan import (
    Floorplan, Vertex, Wall, Door, Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC
)

with Floorplan("Third Floor") as fp:
    h_0 = HC(0)
    h_50 = HC(50)
    h_250 = HC(250)
    h_400 = HC(400)
    v_0 = VC(0)
    v_250 = VC(250)
    v_350 = VC(350)
    v_450 = VC(450)

    v_0_0 = Vertex("Balcony TL", constraints=[h_0, v_0])
    v_0_250 = Vertex("Balcony TR", constraints=[h_0, v_250])
    v_50_0 = Vertex("Reception TL", constraints=[h_50, v_0])
    v_50_250 = Vertex("Reception TR", constraints=[h_50, v_250])
    v_50_350 = Vertex("Bedroom1 TR", constraints=[h_50, v_350])
    v_50_450 = Vertex("Bedroom2 TR", constraints=[h_50, v_450])
    v_250_250 = Vertex("Bedroom1 BL", constraints=[h_250, v_250])
    v_250_350 = Vertex("Hallway TL", constraints=[h_250, v_350])
    v_250_450 = Vertex("Bathroom TL", constraints=[h_250, v_450])
    v_400_0 = Vertex("Reception BL", constraints=[h_400, v_0])
    v_400_250 = Vertex("Reception BR", constraints=[h_400, v_250])
    v_400_350 = Vertex("Bathroom BL", constraints=[h_400, v_350])
    v_400_450 = Vertex("Bathroom BR", constraints=[h_400, v_450])

    balcony_top = Wall("Balcony Top", start_vertex=v_0_0, end_vertex=v_0_250)
    balcony_left = Wall("Balcony Left", start_vertex=v_0_0, end_vertex=v_50_0)
    balcony_right = Wall("Balcony Right", start_vertex=v_0_250, end_vertex=v_50_250)
    balcony_bottom = Wall("Balcony Bottom", start_vertex=v_50_0, end_vertex=v_50_250)
    
    reception_top = Wall("Reception Top", start_vertex=v_50_0, end_vertex=v_50_250)
    reception_right_top = Wall("Reception Right Top", start_vertex=v_50_250, end_vertex=v_250_250)
    reception_right_bottom = Wall("Reception Right Bottom", start_vertex=v_250_250, end_vertex=v_400_250)
    reception_bottom = Wall("Reception Bottom", start_vertex=v_400_0, end_vertex=v_400_250)
    reception_left = Wall("Reception Left", start_vertex=v_50_0, end_vertex=v_400_0)
    
    bedroom1_top = Wall("Bedroom1 Top", start_vertex=v_50_250, end_vertex=v_50_350)
    bedroom1_right = Wall("Bedroom1 Right", start_vertex=v_50_350, end_vertex=v_250_350)
    bedroom1_bottom = Wall("Bedroom1 Bottom", start_vertex=v_250_250, end_vertex=v_250_350)
    bedroom1_left = Wall("Bedroom1 Left", start_vertex=v_50_250, end_vertex=v_250_250)
    
    bedroom2_top = Wall("Bedroom2 Top", start_vertex=v_50_350, end_vertex=v_50_450)
    bedroom2_right = Wall("Bedroom2 Right", start_vertex=v_50_450, end_vertex=v_250_450)
    bedroom2_bottom = Wall("Bedroom2 Bottom", start_vertex=v_250_350, end_vertex=v_250_450)
    bedroom2_left = Wall("Bedroom2 Left", start_vertex=v_50_350, end_vertex=v_250_350)
    
    bathroom_top = Wall("Bathroom Top", start_vertex=v_250_350, end_vertex=v_250_450)
    bathroom_right = Wall("Bathroom Right", start_vertex=v_250_450, end_vertex=v_400_450)
    bathroom_bottom = Wall("Bathroom Bottom", start_vertex=v_400_350, end_vertex=v_400_450)
    bathroom_left = Wall("Bathroom Left", start_vertex=v_250_350, end_vertex=v_400_350)

    Door("Balcony Sliding", wall=balcony_bottom, position=Pos.CENTERED, width=50)
    Door("Bedroom1 Door", wall=bedroom1_left, position=100, width=30)
    Door("Bedroom2 Door", wall=bedroom2_left, position=100, width=30)
    Door("Bathroom Door", wall=bathroom_left, position=50, width=25)
    
    Window("Balcony Window 1", wall=balcony_top, position=50, width=30)
    Window("Balcony Window 2", wall=balcony_top, position=120, width=30)
    Window("Balcony Window 3", wall=balcony_top, position=190, width=30)
    Window("Bedroom1 Window", wall=bedroom1_top, position=Pos.CENTERED, width=40)
    Window("Bedroom2 Window", wall=bedroom2_top, position=Pos.CENTERED, width=40)
    Window("Bathroom Window", wall=bathroom_right, position=Pos.CENTERED, width=35)