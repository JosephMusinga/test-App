def hex_to_vb_color(hex_color):
    # Ensure the input is a valid hex color string
    if not isinstance(hex_color, str) or not hex_color.startswith('#') or len(hex_color) != 7:
        raise ValueError("Input should be a string in the format '#RRGGBB'")
    
    # Extract the red, green, and blue components from the input hex color
    rr = hex_color[1:3]
    gg = hex_color[3:5]
    bb = hex_color[5:7]
    
    # Construct the VB hex color in &HBBGGRR format
    vb_hex_color = f"&H{bb}{gg}{rr}"
    
    return vb_hex_color

# Example usage:
hex_color = "#1A2B3C"
vb_color = hex_to_vb_color(hex_color)
print(vb_color)  # Output: &H3C2B1A
