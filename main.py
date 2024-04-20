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
    # Validate if a video file is uploaded
    if not input_video:
      return render_template('transcribe.html', error="Please upload a valid video file.")
  
    input_video_name = os.path.splitext(input_video.filename)[0]
    # Save the video file
    input_video.save(f'uploads/{input_video_name}.mp4')  # Assuming uploads folder exists

    # Call the extract_audio function
    extracted_audio = extract_audio(f'uploads/{input_video}')

    # Handle successful or failed extraction
    if extracted_audio:
      return render_template('success.html', audio_file=extracted_audio)
    else:
      return render_template('index.html', error="Audio extraction failed.")

  return render_template('index.html')

def extract_audio(input_video):
    
  input_video_name = input_video.replace(".mp4", "")
  extracted_audio = f"audio-{input_video_name}.wav"
  if not os.path.exists(input_video):
    print("Error: Input video does not exist at all.")
    return None
  stream = ffmpeg.input(input_video)
  stream = ffmpeg.output(stream, extracted_audio)
  ffmpeg.run(stream, overwrite_output=True)
  
  if not os.path.exists(extracted_audio):
    print("Error: Audio extraction failed.")
    return None
  return extracted_audio
 

if(__name__ == "__main__"):
    app.run(debug=True)
