from pydub import AudioSegment

# Load the audio file
audio = AudioSegment.from_file("martin.mp4")

# Extract the first 20 seconds
first_20_seconds = audio[:20000]  # 20 seconds * 1000 milliseconds/second

# Export the extracted segment to a new file
first_20_seconds.export(out_f="outNow.mp4", format="mp4")
