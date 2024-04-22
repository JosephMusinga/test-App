import subprocess
import time
import math
import ffmpeg
import os

import whisper

def extract_audio(input_video):
   
    input_video_name = input_video.replace(".mxp4", "")
    extracted_audio = f"audio-{input_video_name}.wav"
    # if not os.path.exists(input_video):
    #   print("Error: Input video does not exist at all.")
    #   return None
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    
    if not os.path.exists(extracted_audio):
      print("Error: Audio extraction failed.")
      return None
    return extracted_audio

extract_audio('martin.mp4')