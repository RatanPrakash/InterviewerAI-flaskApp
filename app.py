from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from interview import InterviewerAI, context_reset

app = Flask(__name__)
app.secret_key = '###InterviewerSecretKey--193834792jgfjfjhgjjhgjhgtsd38749287498aksjdfhksjdhfkdjhdskjhfksdhf-------'



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
    return jsonify({'ai_response': ai_answer})

@app.route('/save_chat_history', methods=['POST'])
def save_chat_history():
    print("chat history saving function called.")
    import datetime
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

if __name__ == '__main__':
    app.run(debug=True)
