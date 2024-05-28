import math
import os
import customtkinter
from CTkColorPicker import *
import shutil
import subprocess
import ffmpeg
import whisper
import tkinter
import re



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
        mainApp.add_captions_to_video_checkbox.select()
        mainApp.main_label.configure(text="Process Complete")
        print("successfully added hard subtitles")
        
    #filedialog for exporting video   
    output_filename = customtkinter.filedialog.asksaveasfilename(
        initialfile=f"output-{copied_video}",
        title="Save Output Video",
        filetypes=[("MP4 files", "*.mp4")]
    )
    
    if output_filename:
        shutil.move(output_video, output_filename)
        print(f"Output video saved to: {output_filename}")
    else:
        print("Output video generation cancelled.")


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
    font_style_var = tkinter.StringVar()
    font_style_var.set(value="Arial")
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
    
    font_size_var = tkinter.StringVar()
    font_size_var.set(value=16)
    font_size_var.trace_add("write", update_font_size_var) 
    font_size_combobox = customtkinter.CTkComboBox(master=toplevel2, values=font_size_list(), variable=font_size_var)
    font_size_combobox.grid(row=1, column=1, padx=5, pady=5)

    # Bold Button
    bold_label = customtkinter.CTkLabel(master=toplevel2, text="Bold:")
    bold_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    
    def update_bold_var(_=None):
        selected_value = bold_segmented.get()
        if selected_value == "Bold":
            bold_var.set(value=1)
        else:
            bold_var.set(value=0)
        print("Bold:", selected_value, bold_var)
    
    bold_var = tkinter.IntVar()
    bold_var.set(value=0)
    bold_segmented = customtkinter.CTkSegmentedButton(master=toplevel2, values=["Bold", "Not Bold"], command=update_bold_var)
    bold_segmented.set("Not Bold")
    bold_segmented.grid(row=2, column=1, padx=5, pady=5)
    
    # Italic Button
    italic_label = customtkinter.CTkLabel(master=toplevel2, text="Italic:")
    italic_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    
    def update_italic_var(_=None):
        selected_value = italic_segmented.get()
        if selected_value == "Italic":
            italic_var.set(value=1)
        else:
            italic_var.set(value=0)
        print("Italic:", selected_value, italic_var)
    
    italic_var = tkinter.IntVar()
    italic_var.set(value=0)
    italic_segmented = customtkinter.CTkSegmentedButton(master=toplevel2, values=["Italic", "Not Italic"], command=update_italic_var)
    italic_segmented.set("Not Italic")
    italic_segmented.grid(row=3, column=1, padx=5, pady=5)
    
    # Color Buttons
    def pick_color(button, color_option):
        pick_color = AskColor()
        if pick_color:
            color = pick_color.get()
            button.configure(**{color_option: color})
            print(f"pick color check: {color}")
            return color
        return None
    
    # Primary Color
    primary_color_label = customtkinter.CTkLabel(master=toplevel2, text="Text Color:")
    primary_color_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")

    global primary_color 
    primary_color = '&Hffffff'
    
    def update_primary_color():
        global primary_color
        print(f"unchanged: {primary_color}")
        new_color = pick_color(primary_color_button, 'fg_color')
        if new_color:
            primary_color = new_color  # Assign the returned color
            print(f"update check: {primary_color}")
    
        
    primary_color_button = customtkinter.CTkButton(master=toplevel2, text="Pick Color", command=update_primary_color)
    primary_color_button.grid(row=4,column=1, padx=5, pady=5)
    
    #Outline(background) color frame
    outline_frame = customtkinter.CTkFrame(toplevel2)
    outline_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    
    #Outline label 
    outline_color_label = customtkinter.CTkLabel(outline_frame, text="Background:")
    outline_color_label.grid(row=0, column=0, padx=5, pady=5)
    
    #Outline switch
    def update_background_var(_=None):
        selected_value = background_segmented.get()
        if selected_value == "On":
            background_var.set(value=3)
        else:
            background_var.set(value=1)
        print("Background:", selected_value, background_var)
    
    background_var = tkinter.IntVar()
    background_var.set(value=1)
    
    background_segmented = customtkinter.CTkSegmentedButton(outline_frame, values=["On", "Off"], command=update_background_var)
    background_segmented.set("Off")
    background_segmented.grid(row=0, column=1, padx=5, pady=5)
    
    #Outline Button
    global outline_color
    outline_color = "&H0"
    
    def update_outline_color():
        global outline_color
        print(f"unchanged: {outline_color}")
        new_color = pick_color(outline_color_button, 'fg_color')
        if new_color:
            outline_color = new_color  # Assign the returned color
            print(f"update check: {outline_color}")
    
    outline_color_button = customtkinter.CTkButton(outline_frame, text="Pick Color", command=update_outline_color)
    outline_color_button.grid(row=0, column=2, padx=5, pady=5)
    
    # Position Button
    position_label = customtkinter.CTkLabel(master=toplevel2, text="Position:")
    position_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
    
    def update_positon_var(_=None):
        selected_value = position_segmented.get()
        if selected_value == "Center":
            position_var.set(value=5)
        elif selected_value == "Top":
            position_var.set(value=8)
        else:
            position_var.set(value=2)
        print("Position:", selected_value, position_var)
    
    position_var = tkinter.IntVar()
    position_var.set(value=2)
    position_segmented = customtkinter.CTkSegmentedButton(master=toplevel2, values=["Bottom", "Center", "Top"], command=update_positon_var)
    position_segmented.set("Bottom")
    position_segmented.grid(row=6, column=1, padx=5, pady=5)
    
    
    def modifications_section(text, font_style, font_size, p_color, out_color, bold, italic, background, position):
        
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
                style_parts[15] = background or style_parts[15]
                style_parts[18] = position or style_parts[18]
                
                lines[i] = ",".join(style_parts)
                break  
        return "\n".join(lines)


    def apply_changes():
        with open(ass_file, "r") as f:
            text = f.read()

        font_style = font_style_var.get()
        print(f"font style: {font_style}")
        
        font_size = font_size_var.get()
        print(f"font size: {font_size}")
        
        def hex_to_vb_color(hex_color):
            
            rr = hex_color[1:3]
            gg = hex_color[3:5]
            bb = hex_color[5:7]
            vb_hex_color = f"&H{bb}{gg}{rr}"
            
            return vb_hex_color
        
        
        p_color = hex_to_vb_color(primary_color)
        print(f"primary: {p_color}")
        
        out_color = hex_to_vb_color(outline_color)
        print(f"out color: {out_color}")
        
        bold = str(bold_var.get())
        print(f"bold: {bold}")
        
        italic = str(italic_var.get())
        print(f"italic: {italic}")
        
        background = str(background_var.get())
        print(f"background: {background_var}")
        
        position = str(position_var.get())
        print(f"bold: {position}")

        modified_text = modifications_section(text, font_style, font_size, p_color, out_color, bold, italic, background, position)

        with open(ass_file, "w") as f:
            f.write(modified_text)
            mainApp.customize_captions_checkbox.select()
            mainApp.main_label.configure(text="Using Customized Caption Apperances")
            print("Successfully Customized Captions")
            toplevel2.destroy()
            
    def destroy_toplevel2():
        toplevel2.destroy()
        mainApp.customize_captions_checkbox.select()
        mainApp.main_label.configure(text="Using Default Caption Apperances")
        pass
            

    cancel_button = customtkinter.CTkButton(master=toplevel2, text="Use Defaults", fg_color="gray", command=destroy_toplevel2)
    cancel_button.grid(row=8, column=0, padx=5, pady=5)

    apply_modifications_button = customtkinter.CTkButton(master=toplevel2, text="Apply Changes", command=apply_changes) #
    apply_modifications_button.grid(row=8, column=1, padx=5, pady=5, sticky="e")
    
   
def display_transcript():
    toplevel = customtkinter.CTkToplevel()
    toplevel.geometry("500x400")
    toplevel.title("Transcript")

    #function to edit the transcript text
    def modify_transcript_text():
        
        def format_time(time_str):
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1]) + hours * 60
            seconds = float(parts[2])
            return f'{minutes:.0f}:{seconds:.2f}'

        output = []
        
        with open(ass_file, 'r') as file:
            for line in file:
                if line.startswith("Dialogue:"):
                    match = re.match(r"Dialogue: \d,(\d+:\d+:\d+\.\d+),\d+:\d+:\d+\.\d+,Default,,\d,\d,\d,,(.*)", line)
                    if match:
                        start_time = format_time(match.group(1))
                        text = match.group(2).replace('\\N', ' ')  # Replace newlines in .ass with spaces
                        output.append(f"[{start_time}] - {text}")
        
        return "\n".join(output)
    
    #saving the edits
    def save_modified_transcript_text():
        edited_text = textbox.get("0.0", customtkinter.END)
        
        lines = edited_text.split('\n')
        extracted_text = [line.split(' - ', 1)[1] if ' - ' in line else '' for line in lines]

        
        ass_file_path = ass_file  # replace with your file path

        with open(ass_file_path, 'r') as file:
            ass_file_content = file.read()

        # Split the .ass file content into lines
        ass_lines = ass_file_content.split('\n')

        # Step 3: Replace dialogue lines
        new_ass_lines = []
        extracted_index = 0

        for line in ass_lines:
            if line.startswith('Dialogue:') and extracted_index < len(extracted_text):
                parts = line.split(',', 9)
                if len(parts) == 10:
                    parts[9] = extracted_text[extracted_index]
                    extracted_index += 1
                new_ass_lines.append(','.join(parts))
            else:
                new_ass_lines.append(line)

        new_ass_content = '\n'.join(new_ass_lines)

        # Step 4: Write the updated content back to the .ass file
        with open(ass_file_path, 'w') as file:
            file.write(new_ass_content)
            toplevel.destroy()
        
        mainApp.main_label.configure(text="Using Edited Captions")    
    
    textbox = customtkinter.CTkTextbox(master=toplevel, width=500, height=350)
    textbox.configure(font=("Verdana",13))
    textbox.grid(row=0, column=0, columnspan=2)
    textbox.insert("0.0", modify_transcript_text())
    
    def destroy_toplevel():
        toplevel.destroy()
        mainApp.main_label.configure(text="Using Generated Captions")
    
    cancel_button = customtkinter.CTkButton(master=toplevel, text="Cancel", fg_color="gray", command=destroy_toplevel)
    cancel_button.grid(row=1, column=0, padx=5, pady=5)
    
    save_button = customtkinter.CTkButton(master=toplevel, text="Save Changes", command=save_modified_transcript_text)
    save_button.grid(row=1, column=1, padx=5, pady=5)

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
        self.title("VIDEO CAPTION GENERATOR")
        self.geometry("450x600")
        self.grid_columnconfigure((0, 1), weight=1)
        self.resizable(False, False)
        
        self.main_label = customtkinter.CTkLabel(self, text="No item selected. Please select a video to start")
        self.main_label.grid(row=0, column=0, padx=20, pady=50, columnspan=4 ,sticky="ew")

        self.open_file_button = customtkinter.CTkButton(self, text="Open File", command=self.open_file)
        self.open_file_button.grid(row=1, column=0, padx=20, pady=20, sticky="e")
        
        self.open_file_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED, fg_color="green")
        self.open_file_checkbox.grid(row=1, column=3)

        self.generate_transcript_button_state_var = "normal"
        self.generate_transcript_button = customtkinter.CTkButton(self, text="Generate Transcript", command=self.transcribe, state=self.generate_transcript_button_state_var)
        self.generate_transcript_button.grid(row=2, column=0, padx=20, pady=20, sticky="e")
        
        self.generate_transcript_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED, fg_color="green")
        self.generate_transcript_checkbox.grid(row=2, column=3)
        
        self.customize_captions_button_state_var = "disabled"
        self.customize_captions_button = customtkinter.CTkButton(self, text="Customize Appearance", command=customize_transcript, state=self.customize_captions_button_state_var)
        self.customize_captions_button.grid(row=3, column=0, padx=20, pady=20, sticky="e")
        
        self.customize_captions_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED, fg_color="green")
        self.customize_captions_checkbox.grid(row=3, column=3)
        
        self.add_captions_to_video_button_state_var = "disabled"
        self.add_captions_to_video_button = customtkinter.CTkButton(self, text="Add captions to video", command=add_subtitle_to_video, state=self.add_captions_to_video_button_state_var)
        self.add_captions_to_video_button.grid(row=4, column=0, padx=20, pady=20, sticky="e")
        
        self.add_captions_to_video_checkbox = customtkinter.CTkCheckBox(self, text=None, border_color="gray", state=tkinter.DISABLED, fg_color="green")
        self.add_captions_to_video_checkbox.grid(row=4, column=3)
        
        self.toplevel_window = None
        self.copied_video = 'None' 
    
    
    #activate button
    def change_button_state(button):
        activation = "normal"
        button = activation
    
        
    def open_file(self):
        filepath = customtkinter.filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("Video Files", "*.mp4")]
        )

        if filepath:
            filename = os.path.basename(filepath)

            try:
                # Overwrite existing file with shutil.move
                shutil.copy(filepath, filename)
                self.copied_video = filename
                self.open_file_checkbox.select()
                self.main_label.configure(text=f"You have selected: {filename}")
                # self.activate_button(self.generate_transcript_button)
                self.generate_transcript_button_state_var = "normal"
                print(self.generate_transcript_button_state_var)
                print(f"File copied to: {filename}")
               
                
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
        result = model.transcribe(audio_file)
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
        self.generate_transcript_checkbox.select()
        self.main_label.configure(text="Transcript has been generated successfully")

        display_transcript()

        return language, segments, self.copied_video

        
mainApp = App()
mainApp.mainloop()
