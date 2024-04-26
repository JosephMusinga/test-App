import math
import os
import customtkinter
import shutil
import subprocess
import ffmpeg
import whisper
import tkinter

def customize_transcript():
    toplevel2 = customtkinter.CTkToplevel()
    toplevel2.geometry("500x400")
    toplevel2.title("Customize Captions")
    
    font_styles = ["Arial", "Times New Roman", "Courier New", "Verdana"]
    font_style_var = tkinter.StringVar(toplevel2)
    font_style_label = customtkinter.CTkLabel(master=toplevel2, text="Font Style:")
    font_style_label.pack()
    font_style_combobox = customtkinter.CTkComboBox(master=toplevel2, values=font_styles, variable=font_style_var)
    font_style_combobox.pack()

    # Font Size Combobox
    font_sizes = range(8, 36)  # Font sizes from 8 to 35
    font_size_var = tkinter.IntVar(toplevel2)
    font_size_label = customtkinter.CTkLabel(master=toplevel2, text="Font Size:")
    font_size_label.pack()
    font_size_combobox = customtkinter.CTkComboBox(master=toplevel2, values=font_sizes, variable=font_size_var)
    font_size_combobox.pack()
    

    # Bold & Italic Radio Buttons
    bold_var = tkinter.BooleanVar(toplevel2)
    italic_var = tkinter.BooleanVar(toplevel2)
    bold_radio = customtkinter.CTkRadioButton(master=toplevel2, variable=bold_var, text="Bold")
    bold_radio.pack(padx=5, pady=5)
    italic_radio = customtkinter.CTkRadioButton(master=toplevel2, variable=italic_var, text="Italic")
    italic_radio.pack(padx=5, pady=5)

    # Color Input Fields
    primary_color_label = customtkinter.CTkLabel(master=toplevel2, text="Primary Color:")
    primary_color_label.pack(padx=5, pady=5)
    primary_color_entry = customtkinter.CTkEntry(master=toplevel2, width=10)
    primary_color_entry.pack(padx=5, pady=5)

    # secondary_color_label = customtkinter.CTkLabel(master=toplevel2, text="Secondary Color (Optional):")
    # secondary_color_label.pack(padx=5, pady=5)
    # secondary_color_entry = customtkinter.CTkEntry(master=toplevel2, width=10)
    # secondary_color_entry.pack(padx=5, pady=5)

    # outline_color_label = customtkinter.CTkLabel(master=toplevel2, text="Outline Color (Optional):")
    # outline_color_label.pack(padx=5, pady=5)
    # outline_color_entry = customtkinter.CTkEntry(master=toplevel2, width=10)
    # outline_color_entry.pack(padx=5, pady=5)

    # back_color_label = customtkinter.CTkLabel(master=toplevel2, text="Back Color (Optional):")
    # back_color_label.pack(padx=5, pady=5)
    # back_color_entry = customtkinter.CTkEntry(master=toplevel2, width=10)
    # back_color_entry.pack(padx=5, pady=5)

    # Modify Button (for illustration only)
    modify_button = customtkinter.CTkButton(master=toplevel2, text="Modify Style (No action yet)")
    modify_button.pack(padx=5, pady=5)
    
    

def display_transcript(transcript_text):
    # Create a Toplevel window
    toplevel = customtkinter.CTkToplevel()
    toplevel.geometry("500x400")
    toplevel.title("Transcript")

    # Create a text widget to display the transcript
    transcript_label = customtkinter.CTkLabel(toplevel, text=transcript_text, text_color="white")
    transcript_label.pack(padx=20, pady=20)

    # Run the Toplevel window
    toplevel.mainloop()

def format_time(seconds):
    # Convert seconds to hours, minutes, and milliseconds
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    # Format time string
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
    return formatted_time

# Function to generate subtitle file from transcribed segments
def generate_subtitle_file(language, segments, video_name):
    srt_file = f"sub-{os.path.splitext(video_name)[0]}.{language}.srt"  
    ass_file = f"sub-{os.path.splitext(video_name)[0]}.{language}.ass"  
    
    text = ""
    # Generate subtitle text with segment start and end times
    for index, segment in enumerate(segments):
        segment_start = format_time(segment["start"])  # Accessing start time using dictionary key
        segment_end = format_time(segment["end"])  # Accessing end time using dictionary key
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment['text']} \n"  # Accessing text using dictionary key
        text += "\n"
    # Write subtitle text to file
    f = open(srt_file, "w")
    f.write(text)
    f.close()
    
    command = ["ffmpeg", "-i", srt_file, ass_file]
    subprocess.run(command, check=True)
    
    try:
        os.remove(srt_file)
        print(f"Temporary audio file deleted: {srt_file}")
    except FileNotFoundError:
        print(f"Audio file not found: {srt_file} (might have already been deleted)")

    return ass_file

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.button_1 = customtkinter.CTkButton(self, text="Open File", command=self.open_file)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.label = customtkinter.CTkLabel(self, text="No item selected", text_color="white")
        self.label.pack(padx=20, pady=20)

        self.button_2 = customtkinter.CTkButton(self, text="Generate Transcript", command=self.transcribe)
        self.button_2.pack(side="top", padx=20, pady=20)
        
        self.button_3 = customtkinter.CTkButton(self, text="Customize Captions", command=customize_transcript)
        self.button_3.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None
        self.copied_video = None  # Track the copied video path

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
                self.label.configure(text=f"You have selected: {filename}")  # Update label with filename
                print(f"File copied to: {filename}")
            except Exception as e:  # Handle potential errors (optional)
                self.label.configure(text="Error copying file")  # Update label with error message
                print(f"Error copying file: {e}")
        else:
            self.label.configure(text="No item selected")  # Update label for no selection

    def extract_audio(self):
        if self.copied_video is None:
            print("Error: No video selected or copied yet.")
            return None

        extracted_audio = f"audio-{os.path.splitext(self.copied_video)[0]}.wav"  # Use filename without extension

        # Check if the input video exists
        if not os.path.exists(self.copied_video):
            print("Error: Input video does not exist.")
            return None

        # Use ffmpeg to extract audio from the video
        stream = ffmpeg.input(self.copied_video)
        stream = ffmpeg.output(stream, extracted_audio)
        ffmpeg.run(stream, overwrite_output=True)

        # Check if audio extraction is successful
        if not os.path.exists(extracted_audio):
            print("Error: Audio extraction failed.")
            return None

        return extracted_audio

    def transcribe(self):
        audio_file = self.extract_audio()
        if audio_file is None:
            self.label.configure(text="Error: Audio extraction failed or no video selected.")
            return

        # Check if audio file exists
        if not os.path.exists(audio_file):
            print("Error: Audio file does not exist.")
            return

        model = whisper.load_model("base")
        # Get the result from transcribe method
        result = model.transcribe(audio_file)
        # Extract segments from the result
        segments = result["segments"]  # Assuming segments are stored in the 'segments' key
        # Access language if available
        language = result.get("language", None)
        print("Transcription language:", language)
        segments = list(segments)
        
        # Delete the audio file after processing
        try:
            os.remove(audio_file)
            print(f"Temporary audio file deleted: {audio_file}")
        except FileNotFoundError:
            print(f"Audio file not found: {audio_file} (might have already been deleted)")

        subtitle_file = generate_subtitle_file(language, segments, self.copied_video)
        print(f"Subtitle file generated: {subtitle_file}")

        # Print or display the transcript (modify as needed)
        transcript_text = ""
        for segment in segments:
            transcript_text += f"[%.2fs -> %.2fs] {segment['text']}\n" % (segment["start"], segment["end"])
        display_transcript(transcript_text) # Update label with transcript

        
        return language, segments, self.copied_video

        

app = App()
app.mainloop()
