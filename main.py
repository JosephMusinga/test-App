import subprocess
import time
import math
import ffmpeg
import os

import whisper
from flask import Flask, render_template, request

app = Flask(__name__)
 
 
@app.route('/')
def home():
        return render_template('index.html')

@app.route('/transcribe')
def transcribe():
        return render_template('transcribe.html')

@app.route('/customize')
def customize():
        return render_template('customize.html')
    
    
@app.route('/extract_audio', methods=['POST'])
def extract():
    if request.method == 'POST':
        # Get the uploaded video file
        input_video = request.files['video_file']

        # Get the filename without extension
        input_video_name = os.path.splitext(input_video.filename)[0]

        # Save the uploaded video file
        input_video.save(f'{input_video_name}.mp4')  # Assuming uploads folder exists

        # Call the extract_audio function
        extracted_audio = extract_audio(f'{input_video_name}.mp4')

        # Handle successful or failed extraction
        if extracted_audio:
            return render_template('success.html', audio_file=extracted_audio)
        else:
            return render_template('index.html', error="Audio extraction failed.")

    return render_template('index.html')

def extract_audio(input_video):
    extracted_audio = f"audio-{os.path.splitext(input_video)[0]}.wav"
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

 

if(__name__ == "__main__"):
    app.run(debug=True)
