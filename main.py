import math
import os
import customtkinter
import shutil
import subprocess
import ffmpeg
import whisper

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
    subtitle_file = f"sub-{os.path.splitext(video_name)[0]}.{language}.srt"  
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
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    # result = convert_subtitle_format(subtitle_file, subtitle_file1)  # Optional for ASS format conversion
    return subtitle_file

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

        # Print or display the transcript (modify as needed)
        transcript_text = ""
        for segment in segments:
            transcript_text += f"[%.2fs -> %.2fs] {segment['text']}\n" % (segment["start"], segment["end"])
        self.label.configure(text=transcript_text)  # Update label with transcript

        # Generate subtitle file
        subtitle_file = generate_subtitle_file(language, segments, self.copied_video)
        print(f"Subtitle file generated: {subtitle_file}")

        # Return language and segments (optional for further processing)
        return language, segments, self.copied_video

        

app = App()
app.mainloop()
