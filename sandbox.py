def get_user_input():
  """
  Prompts the user for font style, size, and other style options.
  """
  font_style = input("Enter desired font style (e.g., Arial, Times New Roman): ")
  font_size = int(input("Enter desired font size (integer): "))
  modify_bold = input("Modify bold (y/n)? ").lower() == 'y'
  modify_italic = input("Modify italic (y/n)? ").lower() == 'y'
  primary_color = pick_color("Enter desired primary color (e.g., white): ")
  secondary_color = pick_color("Enter desired secondary color (optional, press enter to skip): ")
  outline_color = pick_color("Enter desired outline color (optional, press enter to skip): ")
  back_color = pick_color("Enter desired background color (optional, press enter to skip): ")
  return font_style, font_size, modify_bold, modify_italic, primary_color, secondary_color, outline_color, back_color

def pick_color(message):
  """
  Prompts the user for a color and returns it in the format &Hrrggbb.
  """
  while True:
    color = input(message).strip().lower()
    if not color:
      return None  # User skipped color selection
    try:
      # Validate and convert color to hex format with leading zeroes (e.g., #ffffff -> &Hffffff)
      if color.startswith("#"):
        color = color[1:]
      color = format(int(color, 16), '06x').upper()
      return "&H" + color
    except ValueError:
      print("Invalid color format. Please enter a valid color name or hex code (e.g., white, #ffffff).")

def modify_style_section(text, font_style, font_size, modify_bold, modify_italic, primary_color, secondary_color, outline_color, back_color):
  """
  Modifies the [V4+ Styles] section in the text with the user-provided style and size.
  """
  lines = text.splitlines()
  for i, line in enumerate(lines):
    if line.startswith("Style: Default,"):
      # Split the style definition
      style_parts = line.split(",")
      # Update style properties
      style_parts[1] = f'"{font_style}"'  # Font style
      style_parts[2] = str(font_size)  # Font size
      if modify_bold:
        style_parts[7] = str(int(input("Enter desired bold value (0 or 1): ")))  # Bold
      if modify_italic:
        style_parts[8] = str(int(input("Enter desired italic value (0 or 1): ")))  # Italic
      style_parts[4] = primary_color or style_parts[4]  # Primary color (use existing if not provided)
      style_parts[5] = secondary_color or style_parts[5]  # Secondary color (use existing if not provided)
      style_parts[6] = outline_color or style_parts[6]  # Outline color (use existing if not provided)
      style_parts[9] = back_color or style_parts[9]  # Back color (use existing if not provided)
      # Join the modified parts back with comma separators
      lines[i] = ",".join(style_parts)
      break  # Stop after modifying the first occurrence
  return "\n".join(lines)

def main():
  """
  Reads the text file, prompts user for input, modifies the style section, and writes the modified text back to the file.
  """
  with open("sub-martin.en.ass", "r") as f:
    text = f.read()
  
  font_style, font_size, modify_bold, modify_italic, primary_color, secondary_color, outline_color, back_color = get_user_input()
  modified_text = modify_style_section(text, font_style, font_size, modify_bold, modify_italic, primary_color, secondary_color, outline_color, back_color)
  
  
  with open("custom_captions.ass", "w") as f:
    f.write(modified_text)
  
  print("Successfully modified the font style and size in your .ass file!")

if __name__ == "__main__":
  main()
