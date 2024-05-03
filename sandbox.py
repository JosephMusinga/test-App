import customtkinter
import shutil
import os

def test():
  print(app.copied_video)

class App(customtkinter.CTk):
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("250x200")

        self.open_file_button = customtkinter.CTkButton(self, text="Open File", command=self.open_file)
        self.open_file_button.pack(side="top", padx=20, pady=20)
        
        self.open_file_buttona = customtkinter.CTkButton(self, text="check again", command=test)
        self.open_file_buttona.pack(side="top", padx=20, pady=20)
        
        self.copied_video = 'None'
        
  def open_file(self):
        filepath = customtkinter.filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("Video Files", "*.mp4")]
        )
        if filepath:
            filename = os.path.basename(filepath)  # Extract filename

            try:
                shutil.copy(filepath, filename)  # Copy the file using filename
                self.copied_video = filename
                print(f"{self.copied_video} at check 1")
                
            except Exception as e:  # Handle potential errors (optional)
                print(text="Error copying file")
            
  
app = App()
app.mainloop()