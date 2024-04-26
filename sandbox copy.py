from customtkinter import CTkColorPicker
import customtkinter

primary_color_var = tk.StringVar(toplevel2)  # Global variable to store the chosen color

def pick_primary_color():
    """
    Opens a color picker and sets the chosen color in the primary_color_var variable.
    """
    color = CTkColorPicker(master=toplevel2).show()  # Open the color picker
    if color:
        primary_color_var.set(color)  # Set the color variable if a color is chosen

primary_color_label = customtkinter.CTkLabel(master=toplevel2, text="Primary Color:")
primary_color_label.pack(padx=5, pady=5)

primary_color_button = customtkinter.CTkButton(
    master=toplevel2, text="Pick", command=pick_primary_color
)
primary_color_button.pack(padx=5, pady=5)
