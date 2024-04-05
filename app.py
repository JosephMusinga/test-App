from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import whisper

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

# @socketio.on('message')
# def handle_message(message):
#     print('Received message: ' + message)
#     emit('message', message, broadcast=True)

def send_transcript(transcript):
    emit('transcript', transcript, broadcast=True)

@socketio.on('transcribe_audio')
def handle_transcribe_audio():
    transcribe_and_send()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port="5000", debug=True)