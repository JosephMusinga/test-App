import math
import os
import customtkinter
from CTkColorPicker import *
import shutil
import subprocess
import ffmpeg
import whisper
import tkinter


def add_subtitle_to_video():
    
    copied_video = mainApp.copied_video
    video_input_stream = ffmpeg.input(copied_video)
    subtitle_input_stream = ffmpeg.input(ass_file)
    output_video = f"output-{copied_video}.mp4"
    subtitle_track_title = ass_file.replace(".ass", "")
    
    soft_subtitle = False
    subtitle_language = 'en'
    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
        print("successfully added soft subtitles")
        
    else:
        # Add hard subtitles
        stream = ffmpeg.output(video_input_stream, output_video,
                               vf=f"subtitles={ass_file}")
        ffmpeg.run(stream, overwrite_output=True)
        print("successfully added hard subtitles")


def customize_transcript():
    toplevel2 = customtkinter.CTkToplevel()
    toplevel2.title("Customize Captions")
    toplevel2.grid_columnconfigure((0, 1, 2), weight=1)
    toplevel2.grid_rowconfigure((8), weight=2)
    toplevel2.resizable(False, False)
    
    #customize window startup positon on screen
    w = 400 
    h = 500
    
    ws = toplevel2.winfo_screenwidth() # width of the screen
    hs = toplevel2.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    toplevel2.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    # Font Style combobox
    def update_font_style_var(*args):
        selected_font_style = font_style_var.get()
        print("Selected font style:", selected_font_style)
    
    font_style_label = customtkinter.CTkLabel(master=toplevel2, text="Font Style:")
    font_style_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    
    font_styles = ["Arial", "Times New Roman", "Courier New", "Verdana"]
    font_style_var = tkinter.StringVar(value="Arial")
    font_style_var.trace_add("write", update_font_style_var) 
    font_style_combobox = customtkinter.CTkComboBox(master=toplevel2, values=font_styles, variable=font_style_var)
    font_style_combobox.grid(row=0, column=1, padx=5, pady=5)
    
    # Font Size combobox
    def update_font_size_var(*args):
        selected_font_size = font_size_var.get()
        print("Selected font size:", selected_font_size)

    def font_size_list():
        return [str(i) for i in range(8, 31)]
    
    font_size_label = customtkinter.CTkLabel(master=toplevel2, text="Font Size:")
    font_size_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    
    font_size_var = tkinter.StringVar(value=16)
    font_size_var.trace_add("write", update_font_size_var) 
    font_size_combobox = customtkinter.CTkComboBox(master=toplevel2, values=font_size_list(), variable=font_size_var)
    font_size_combobox.grid(row=1, column=1, padx=5, pady=5)

    # Bold Button
    bold_label = customtkinter.CTkLabel(master=toplevel2, text="Bold:")
    bold_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    
    def update_bold_var(_=None):
        selected_value = bold_segmented.get()
        if selected_value == "Bold":
            bold_var = 1
        else:
            bold_var = 0
        print("Bold:", selected_value, bold_var)
    
    bold_var = tkinter.IntVar(value=0)
    bold_segmented = customtkinter.CTkSegmentedButton(master=toplevel2, values=["Bold", "Not Bold"], command=update_bold_var)
    bold_segmented.set("Not Bold")
    bold_segmented.grid(row=2, column=1, padx=5, pady=5)
    
    # Italic Button
    italic_label = customtkinter.CTkLabel(master=toplevel2, text="Italic:")
    italic_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    
    def update_italic_var(_=None):
        selected_value = italic_segmented.get()
        if selected_value == "Italic":
            italic_var = 1
        else:
            italic_var = 0
        print("Italic:", selected_value, italic_var)
    
    italic_var = tkinter.IntVar(value=0)
    italic_segmented = customtkinter.CTkSegmentedButton(master=toplevel2, values=["Italic", "Not Italic"], command=update_italic_var)
    italic_segmented.set("Not Italic")
    italic_segmented.grid(row=3, column=1, padx=5, pady=5)
    
    # Color Buttons
    def pick_color(button, color_option):
        pick_color = AskColor()
        if pick_color:
            color = pick_color.get()
            button.configure(**{color_option: color})
            return color
        return None
    
    # Primary Color
    def update_primary_color():
        global primary_color
        primary_color = '&Hffffff'
        primary_color = pick_color(primary_color_button, 'fg_color')
        print(primary_color)
        
    primary_color_label = customtkinter.CTkLabel(master=toplevel2, text="Primary Color:")
    primary_color_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")

    primary_color_button = customtkinter.CTkButton(master=toplevel2, text="Pick Color", command=update_primary_color)
    primary_color_button.grid(row=4,column=1, padx=5, pady=5)
    
    #Outline(background) color frame
    outline_frame = customtkinter.CTkFrame(toplevel2)
    outline_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    
    #Outline Switch
    switch_var = customtkinter.StringVar(value="off")
    add_outline_switch = customtkinter.CTkSwitch(outline_frame, text="Add Background", variable=switch_var, onvalue="on", offvalue="off")
    add_outline_switch.grid(row=0, column=0, padx=5, pady=5)
    
    #Outline Button
    def update_outline_color():
        global outline_color
        outline_color = "&H0"
        outline_color = pick_color(outline_color_button, 'fg_color')
        print(outline_color)

    outline_color_button = customtkinter.CTkButton(outline_frame, text="Pick Color", command=update_outline_color)
    outline_color_button.grid(row=0, column=1, padx=5, pady=5)
    
       
    
    def update_secondary_color():
        global secondary_color
        secondary_color = '&Hffffff'
        secondary_color = pick_color(secondary_color_button, 'fg_color')
        print(secondary_color)

    secondary_color_button = customtkinter.CTkButton(master=toplevel2, text="Secondary Color", command=update_secondary_color)
    secondary_color_button.grid(row=6,column=1, padx=5, pady=5)
    
    
    
    # def update_background_color():
    #     global background_color
    #     background_color = "&H0"
    #     background_color = pick_color(background_color_button, 'fg_color')
    #     print(background_color)
    
    # background_color_button = customtkinter.CTkButton(master=toplevel2, text="Background Color", command=update_background_color)
    # background_color_button.grid(row=5,column=1, padx=5, pady=5)
    
    
    def modifications_section(text, font_style, font_size, p_color, out_color, bold, italic):
        """
        Modifies the [V4+ Styles] section in the text with the user-provided style and size.
        """
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("Style: Default,"):
                style_parts = line.split(",")
                style_parts[1] = font_style 
                style_parts[2] = str(font_size)
                style_parts[3] = p_color or style_parts[3]
                style_parts[5] = out_color or style_parts[5] 
                style_parts[7] = bold or style_parts[7]
                style_parts[8] = italic or style_parts[8]
                
                lines[i] = ",".join(style_parts)
                break  
        return "\n".join(lines)


    def apply_changes():
        with open(ass_file, "r") as f:
            text = f.read()
            
        def convert_color_format(var):
            color = var.replace('#', '&H')
            return color

        font_style = font_style_var
        font_size = font_size_var
        
        p_color = convert_color_format(primary_color)
        out_color = convert_color_format(outline_color)
        bold = str(bold_var.get())
        italic = str(italic_var.get())

        modified_text = modifications_section(text, font_style, font_size, p_color, out_color, bold, italic)

        with open(ass_file, "w") as f:
            f.write(modified_text)
            
        print("Successfully modified")
        # success_text = "Customizations applied"
        # App.update_main_label(success_text)

    cancel_button = customtkinter.CTkButton(master=toplevel2, text="Cancel", fg_color="gray") #
    cancel_button.grid(row=8, column=0, padx=5, pady=5)

    apply_modifications_button = customtkinter.CTkButton(master=toplevel2, text="Apply Changes", command=apply_changes) #
    apply_modifications_button.grid(row=8, column=1, padx=5, pady=5, sticky="e")
    
    
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


def generate_subtitle_file(language, segments, video_name):
    srt_file = f"sub-{os.path.splitext(video_name)[0]}.{language}.srt" 
    global ass_file
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
    
    command = ["ffmpeg", "-i", srt_file, "-y",ass_file]
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
        self.title("CAPTION GENERATOR")
        self.geometry("450x600")
        self.grid_columnconfigure((0, 1), weight=1)
        self.resizable(False, False)
        
        self.main_label = customtkinter.CTkLabel(self, text="No item selected. Please select a video to start", text_color="white")
        self.main_label.grid(row=0, column=0, padx=20, pady=50, columnspan=4 ,sticky="ew")

        self.open_file_button = customtkinter.CTkButton(self, text="Open File", command=self.open_file)
        self.open_file_button.grid(row=1, column=0, padx=20, pady=20, sticky="e")
        
        self.open_file_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED)
        self.open_file_checkbox.grid(row=1, column=3)

        self.generate_transcript_button = customtkinter.CTkButton(self, text="Generate Transcript", command=self.transcribe)
        self.generate_transcript_button.grid(row=2, column=0, padx=20, pady=20, sticky="e")
        
        self.generate_transcript_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED)
        self.generate_transcript_checkbox.grid(row=2, column=3)
        
        self.customize_captions_button = customtkinter.CTkButton(self, text="Customize Appearance", command=customize_transcript)
        self.customize_captions_button.grid(row=3, column=0, padx=20, pady=20, sticky="e")
        
        self.customize_captions_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED)
        self.customize_captions_checkbox.grid(row=3, column=3)
        
        self.add_captions_to_video_button = customtkinter.CTkButton(self, text="Add captions to video", command=add_subtitle_to_video)
        self.add_captions_to_video_button.grid(row=4, column=0, padx=20, pady=20, sticky="e")
        
        self.add_captions_to_video_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED)
        self.add_captions_to_video_checkbox.grid(row=4, column=3)
        
        self.toplevel_window = None
        self.copied_video = 'None' 
        
    def open_file(self):
        filepath = customtkinter.filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("Video Files", "*.mp4")]
        )

        if filepath:
            filename = os.path.basename(filepath)  # Extract filename

            try:
                # Overwrite existing file with shutil.move
                shutil.move(filepath, filename)  
                self.copied_video = filename
                self.main_label.configure(text=f"You have selected: {filename}")  # Update main_label with filename
                print(f"File moved to: {filename}")
            except Exception as e:  # Handle potential errors (optional)
                self.main_label.configure(text="Error copying file")  # Update main_label with error message
                print(f"Error copying file: {e}")
        else:
            self.main_label.configure(text="No item selected")  # Update label for no selection

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
            self.main_label.configure(text="Error: Audio extraction failed or no video selected.")
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
        print(f"Transcript file generated: {subtitle_file}")
        self.main_label.configure(text="Transcript has been generated successfully")

        # Print or display the transcript (modify as needed)
        transcript_text = ""
        for segment in segments:
            transcript_text += f"[%.2fs -> %.2fs] {segment['text']}\n" % (segment["start"], segment["end"])
        display_transcript(transcript_text) # Update label with transcript

        return language, segments, self.copied_video

        
mainApp = App()
mainApp.mainloop()
