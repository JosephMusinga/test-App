def convert_color_format(var):
    """Replaces '#' with '&H' in the given color string.

    Args:
        var: The color string in hexadecimal format (e.g., '#636363').

    Returns:
        A new string with '#' replaced by '&H'.
    """

    color = var.replace('#', '&H')  # Assign the replaced string back to color
    return color

new_color = '#636363'
converted_color = convert_color_format(new_color)
print(converted_color) 