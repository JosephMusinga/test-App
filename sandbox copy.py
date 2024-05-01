line = "Style: Default,Arial,16,&Hffffff,&Hffffff,&H0,&H0,0,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1"

if line.startswith("Style: Default,"):
    style_parts = line.split(",")
