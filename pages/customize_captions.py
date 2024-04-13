from customtkinter import CTkFrame, CTkButton, CTkLabel

class CustomizeCaptions(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create UI elements for the main page
        label = CTkLabel(self, text="Customize")
        label.pack()