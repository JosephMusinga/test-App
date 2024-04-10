import time
import math
import ffmpeg
import os

import whisper

input_video = "input.mp4"
input_video_name = input_video.replace(".mp4", "")

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    # Debugging point 1: Check if the input video exists
    if not os.path.exists(input_video):
        print("Error: Input video does not exist.")
        return None
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    # Debugging point 2: Check if audio extraction is successful
    if not os.path.exists(extracted_audio):
        print("Error: Audio extraction failed.")
        return None
    return extracted_audio

def transcribe(audio):
    if not os.path.exists(audio):
        print("Error: Audio file does not exist.")
        return None
    model = whisper.load_model("base")
    result = model.transcribe(audio)  # Get the result from transcribe method
    segments = result["segments"]  # Assuming segments are stored in the 'segments' key
    language = result.get("language", None)  # Access language if available
    print("Transcription language:", language)
    segments = list(segments)
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment["start"], segment["end"], segment["text"]))
    return language, segments

def run():
    extracted_audio = extract_audio()
    if extracted_audio:
        language, segments = transcribe(audio=extracted_audio)
    else:
        print("Error: Audio extraction failed.")
run()
