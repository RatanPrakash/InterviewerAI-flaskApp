from flask import Flask, request, jsonify, render_template
import os
import openai
from dotenv import load_dotenv
from functions import say, speechToText, write_text_to_file
import datetime

app = Flask(__name__)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

context = [{"role": "system",
            "content": """Your name is 'Friday' and you are a helpful Interviewer chat bot who answers in short and crisp sentences. 
            Ask beginner level questions on data science and provide a judgement of the candidate's answers to them correctly. 
            Make sure you ask different questions one by one and get their answers from the candidate. 
            Firstly Greet the user, Introduce yourself and ask them to introduce themselves. \
            Don't jump to technical questions directly. Start with a few HR questions. \
            Ask them to answer the questions in a natural way. \
            After each of their answer, reply in a interview style, correct them if needed and appreciate them if they are right. \
            #Important# \
                DO NOT answer unrelated questions. Stick to the interview process and your role. \
                Be sure you know their name and use their first name in the conversation, occasionally."""}]

def get_completion_from_messages(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9, 
    )
    return response.choices[0].message.content

def InterviewerAI(userResponse):
    context.append({'role':'user', 'content':f"{userResponse}"})
    ai_answer = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{ai_answer}"})
    return ai_answer

@app.route('/')
def index():
    return render_template('interview.html')

@app.route('/interview', methods=['POST'])
def interview():
    user_response = request.json['user_response']
    ai_answer = InterviewerAI(user_response)
    return jsonify({'user_response': user_response, 'ai_response': ai_answer})

if __name__ == "__main__":
    app.run(debug=True)
