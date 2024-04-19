from customtkinter import CTkFrame, CTkButton, CTkLabel

class GenerateCaptions(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create UI elements for the main page
        label = CTkLabel(self, text="Pick a video")
        label.pack()
        
        button2 = CTkButton(self, text="Main", command=lambda: master.show_frame(master.main_page))
        button2.pack(pady=12, padx=10)
        
        button1 = CTkButton(self, text="Next", command=lambda: master.show_frame(master.customize_captions))
        button1.pack(pady=12, padx=10)