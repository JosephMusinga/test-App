import customtkinter  # Import CustomTkinter
from pages.main_page import MainPage

customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('green')

class CaptionApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Caption Generator")
        self.geometry("800x450")

        # Create page frames (instances of your page classes from pages/)
        self.main_page = MainPage(self)
        # self.page1 = Page1(self)
        # self.page2 = Page2(self)

        # Initially show the main page
        self.show_frame(self.main_page)

        # Define navigation buttons (replace with your button creation logic)
        # self.main_page_button = customtkinter.CTkButton(
        #     self, text="Main Page", command=lambda: self.show_frame(self.main_page)
        # )
        # self.main_page_button.pack()
        # # ... buttons for other pages

    def show_frame(self, frame):
        frame.pack(fill="both", expand=True)
        frame.lift()  # Raise the frame to the top

if __name__ == "__main__":
    app = CaptionApp()
    app.mainloop()
