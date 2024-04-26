import customtkinter
import tkinter

window = customtkinter()
window.geometry("400x500")
window.title("ASS Subtitle Style Editor")

# Font Style Combobox
font_styles = ["Arial", "Times New Roman", "Courier New", "Verdana"]
font_style_var = tkinter.StringVar(window)
font_style_label = customtkinter.Label(master=window, text="Font Style:")
font_style_label.pack()
font_style_combobox = customtkinter.ComboBox(master=window, values=font_styles, variable=font_style_var)
font_style_combobox.pack()

# Font Size Combobox
font_sizes = range(8, 36)  # Font sizes from 8 to 35
font_size_var = tkinter.IntVar(window)
font_size_label = customtkinter.Label(master=window, text="Font Size:")
font_size_label.pack()
font_size_combobox = customtkinter.ComboBox(master=window, values=font_sizes, variable=font_size_var)
font_size_combobox.pack()

# Bold & Italic Radio Buttons
bold_var = tkinter.BooleanVar(window)
italic_var = tkinter.BooleanVar(window)
bold_radio = customtkinter.Radiobutton(master=window, variable=bold_var, text="Bold")
bold_radio.pack()
italic_radio = customtkinter.Radiobutton(master=window, variable=italic_var, text="Italic")
italic_radio.pack()

# Color Input Fields
primary_color_label = customtkinter.Label(master=window, text="Primary Color:")
primary_color_label.pack()
primary_color_entry = customtkinter.Entry(master=window, width=10)
primary_color_entry.pack()

secondary_color_label = customtkinter.Label(master=window, text="Secondary Color (Optional):")
secondary_color_label.pack()
secondary_color_entry = customtkinter.Entry(master=window, width=10)
secondary_color_entry.pack()

outline_color_label = customtkinter.Label(master=window, text="Outline Color (Optional):")
outline_color_label.pack()
outline_color_entry = customtkinter.Entry(master=window, width=10)
outline_color_entry.pack()

back_color_label = customtkinter.Label(master=window, text="Back Color (Optional):")
back_color_label.pack()
back_color_entry = customtkinter.Entry(master=window, width=10)
back_color_entry.pack()

# Modify Button (for illustration only)
modify_button = customtkinter.Button(master=window, text="Modify Style (No action yet)")
modify_button.pack()

window.mainloop()
