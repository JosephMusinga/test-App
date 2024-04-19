from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkSlider
from pages.generate_captions import GenerateCaptions
import tkinter
from utils import media_transcription


class MainPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create UI elements for the main page
        label = CTkLabel(self, text="This is the Main Page")
        label.pack()

        # Buttons to navigate to other pages (replace with your button logic)
        button1 = CTkButton(self, text="Generate Caption for Video/Audio", command=lambda: media_transcription.run())
        button1.pack(pady=12, padx=10)
        
        
        
 
    