from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file 
from flask_socketio import SocketIO, emit
from interview import InterviewerAI, context_reset
from functions import speech
import time
import datetime
import os

app = Flask(__name__)
app.secret_key = '###InterviewerSecretKey--193834792jgfjfjhgjjhgjhgtsd38749287498aksjdfhksjdhfkdjhdskjhfksdhf-------'
socketio = SocketIO(app)


@app.route('/')
def index():
    context_reset()
    return render_template('index.html')

UPLOAD_FOLDER = 'userData/resumes/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return 'No file part'
        file = request.files['resume']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('index'))
        

@app.route('/interview', methods=['POST'])
def interview():
    user_response = request.json['user_response']
    ai_answer = InterviewerAI(user_response)
    speech(ai_answer)
    return jsonify({'ai_response': ai_answer, 'audio_url': "FridayReplies/speech.mp3"})

@app.route('/save_chat_history', methods=['POST'])
def save_chat_history():
    print("chat history saving function called.")
    current_datetime = datetime.datetime.now()
    filename = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    chat_history = request.json.get('chat_history')
    if chat_history:
        # Format chat history as text
        chat_text = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        context_reset()
        try:
            # Save chat history to a text file
            with open(f'userData/chatHistory/{filename}.txt', 'w') as file:
                file.write(chat_text)
            return jsonify({'success': True}), 200
        except Exception as e:
            print(e)
            return jsonify({'success': False}), 500
    else:
        return jsonify({'success': False}), 400

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.json['text']
    # Process the text here
    user_response = text
    ai_answer = InterviewerAI(user_response)
    return jsonify({'output': ai_answer})

@app.route('/save_video', methods=['POST'])
def save_video():
    current_datetime = datetime.datetime.now()
    filename = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    try:
        video_file = request.files['video']
        video_file.save(f'userData/interviewRecordings/{filename}.webm')
        return jsonify({'message': 'Video saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_audio')
def get_audio():
    # Call your function that returns the audio file
    audio_file_path = "FridayReplies/speech.mp3"
    return send_file(audio_file_path, mimetype='audio/mpeg', as_attachment=True)

@socketio.on('request_audio')
def stream_audio():
    audio_file_path = "FridayReplies/speech.mp3"  # Your function to get audio file path
    with open(audio_file_path, 'rb') as audio_file:
        while True:
            chunk = audio_file.read()
            if not chunk:
                break
            emit('audio_data', {'chunk': chunk})
            time.sleep(0.1)  # Adjust sleep time as needed



if __name__ == '__main__':
    app.run(debug=True)
