from customtkinter import CTkFrame, CTkButton, CTkLabel

class MainPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create UI elements for the main page
        label = CTkLabel(self, text="This is the Main Page")
        label.pack()

        # Buttons to navigate to other pages (replace with your button logic)
        button1 = CTkButton(self, text="Generate Caption for Video/Audio", command=lambda: master.show_frame(master.page1))
        button1.pack(pady=12, padx=10)
        
        button2 = CTkButton(self, text="Generate Live Captions", command=lambda: master.show_frame(master.page1))
        button2.pack(pady=12, padx=10)
        # ... buttons for other pages
 
