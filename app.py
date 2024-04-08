# Flask app code
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import whisper

from pydub import AudioSegment  
from pydub.playback import play  

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def transcribe_and_send():
    model = whisper.load_model("base")
    result = model.transcribe("martin.mp4")
    transcript = result["text"]
    send_transcript(transcript)
    print(transcript)

def send_transcript(transcript):
    emit('transcript', transcript)  # Broadcasting isn't necessary here

@socketio.on('transcribe_audio')  # Listening for 'transcribe_audio' event from client
def handle_transcribe_audio():
    transcribe_and_send()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
