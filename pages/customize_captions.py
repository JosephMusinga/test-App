from customtkinter import CTkFrame, CTkButton, CTkLabel

class CustomizeCaptions(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create UI elements for the main page
        label = CTkLabel(self, text="Customize Captions")
        label.pack()
        
        button1 = CTkButton(self, text="Next", command=lambda: master.show_frame(master.customize_captions))
        button1.pack(pady=12, padx=10)