import os
import openai
from dotenv import load_dotenv
from functions import say, speechToText, write_text_to_file
import datetime

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_completion_from_messages(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9, 
    )
    return response.choices[0].message.content

context = [{"role": "system",
            "content": """Your name is 'Friday' and you are a helpful Interviewer chat bot who answers in short and crisp sentences. 
            Ask beginner level questions on data science and provide a judgement of the candidate's answers to them correctly. 
            Make sure you ask different questions one by one and get their answers from the candidate. 
            Firstly Greet the user, Introduce yourself and ask them to introduce themselves. \
            Don't jump to technical questions directly. Start with a few HR questions. \
            Ask them to answer the questions in a natural way. \
            After each of their answer, reply in a interview style, correct them if needed and appreciate them if they are right. \
            #Important# \
                DO NOT answer unrelated questions.
                Be sure you know their name and use it in the conversation. """}]

def InterviewerAI(userResponse):
    print("Interviewer A.I., is now being called.")

    context.append({'role':'user', 'content':f"{userResponse}"})
    ai_answer = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{ai_answer}"})
    return ai_answer

questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "What are your weaknesses?",
    "Why do you want to work for this company?",
    "Can you describe a difficult problem you solved?",
    "Where do you see yourself in 5 years?",
    "What is machine Learning?",
    "What is reinforcement learning?",
    "What is supervised and unsupervised learning?",
    "What is a generative AI?",
    "What is computer Vision?"
    # Add more questions as needed
]
def interview():
    print("Welcome to the Interview Bot!")
    print("I'll ask you a few questions. Please respond naturally. \n")
    chat = ["", "", "", ""]
    ai_answer = InterviewerAI("")
    print(ai_answer)
    say(ai_answer)
    chat.append(f"Friday: {ai_answer}")
    while True:
        printChat = "\n".join(chat)
        print(f"CHATS TILL NOW: \n {printChat} \n")
        print("Friday is listening ...")
        # userResponse = speechToText()
        userResponse = input("User: ")
        print(f"USER : {userResponse}")

        if "stop listening" in userResponse.lower():
            say("Alright.")
            break
        if userResponse:
            ai_answer = InterviewerAI(userResponse)
            print(ai_answer)
            say(ai_answer)
            chat.append(f"User: {userResponse}")
            chat.append(f"Friday: {ai_answer}")

    # Format the current date and time as desired for the file name
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    write_text_to_file("\n".join(chat), f"InterviewExperience/Interview_{formatted_datetime}.txt")

    print("\nThank you for the interview!")
    say("Thank you for the interview!")
if __name__ == "__main__":
    pass
