import subprocess
import time
import math
import ffmpeg
import os

import whisper

# Define input video file and its name
input_video = "martin.mp4"
input_video_name = input_video.replace(".mp4", "")

# Function to extract audio from the input video file
def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    # Check if the input video exists
    if not os.path.exists(input_video):
        print("Error: Input video does not exist.")
        return None
    # Use ffmpeg to extract audio from the video
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    # Check if audio extraction is successful
    if not os.path.exists(extracted_audio):
        print("Error: Audio extraction failed.")
        return None
    return extracted_audio

# Function to transcribe the audio
def transcribe(audio):
    if not os.path.exists(audio):
        print("Error: Audio file does not exist.")
        return None
    model = whisper.load_model("base")
    # Get the result from transcribe method
    result = model.transcribe(audio)
    # Extract segments from the result
    segments = result["segments"]  # Assuming segments are stored in the 'segments' key
    # Access language if available
    language = result.get("language", None)
    print("Transcription language:", language)
    segments = list(segments)
    # Print each segment with its start and end times and text
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment["start"], segment["end"], segment["text"]))
    return language, segments

# Function to format time in the required format
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
def generate_subtitle_file(language, segments):
    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    subtitle_file1 = f"sub-{input_video_name}.{language}.ass"
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

    # result = convert_subtitle_format(subtitle_file, subtitle_file1)
    return subtitle_file
    

def convert_subtitle_format(input_file, output_file):
        command = ["ffmpeg", "-i", input_file, output_file]
        subprocess.run(command, check=True)
        

# Function to add subtitle to the video
def add_subtitle_to_video(soft_subtitle, subtitle_file,  subtitle_language):
    # Define input video stream
    video_input_stream = ffmpeg.input(input_video)
    # Define subtitle input stream
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    # Define output video file name
    output_video = f"output-{input_video_name}.mp4"
    subtitle_track_title = subtitle_file.replace(".ass", "")
    # Add soft subtitles if specified
    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        # Add hard subtitles
        stream = ffmpeg.output(video_input_stream, output_video,
                               vf=f"subtitles={subtitle_file}")
        ffmpeg.run(stream, overwrite_output=True)    

# Function to run the entire process
def run():
    # Extract audio from the input video
    extracted_audio = extract_audio()
    # Transcribe the extracted audio
    language, segments = transcribe(audio=extracted_audio)
    # Generate subtitle file from transcribed segments
    subtitle_file = generate_subtitle_file(
        language=language,
        segments=segments
    )
    # Add subtitle to the input video
    add_subtitle_to_video(
        soft_subtitle=True,
        subtitle_file=subtitle_file,
        subtitle_language=language
    )
    
run()
