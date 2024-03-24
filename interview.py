import os
import openai
from dotenv import load_dotenv

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
            "content": """Your name is 'John', a helpful Interviewer chat bot who answers in short and crisp sentences. 
            Ask beginner level questions on data science and provide a judgement of the candidate's answers to them correctly. 
            Make sure you ask different questions one by one and get their answers from the candidate. 
            Firstly Greet the user, Introduce yourself and ask them to introduce themselves. \
            Don't jump to technical questions directly. Start with a few HR questions. \
            Ask them to answer the questions in a natural way. \
            After each of their answer, reply in a interview style, correct them if needed and appreciate them if they are right. \
            #Important# \
                DO NOT answer unrelated questions. Stick to the interview process and your role. \
                Be sure you know their name and use their first name in the conversation, occasionally."""}]

def InterviewerAI(userResponse):
    print("Interviewer A.I., is now being called.")
    context.append({'role':'user', 'content':f"{userResponse}"})
    ai_answer = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{ai_answer}"})
    return ai_answer

def context_reset(resume=""):
    global context
    print("Context reset.")
    if not resume:
        resume = "There is no resume uploaded as of yet. Ask generic questions related to Computer Science to the candidate."
    context = [{"role": "system",
                "content": f"""Your name is 'John', a helpful Interviewer who answers in Interview style. 
                Ask beginner level questions on Computer science and provide a judgement of the candidate's answers to them correctly.
                Prefer Resume based questions. Here is the resume content of the candidate. \ 
                RESUME CONTENT: ```{resume}``` \
                Make sure you ask different questions one by one and get their answers from the candidate. 
                Firstly Greet the user, Introduce yourself and ask them to introduce themselves. \
                Don't jump to technical questions directly. Start with a few HR questions. \
                If you find that the candidate's answer seems interrupted in between and is not complete, ask them to continue. \
                After each of their answer, reply in a interview style, correct them if needed and appreciate them ONLY AND ONLY if they are right. \
                #Important# \
                    DO NOT answer unrelated questions. Stick to the interview process and your role. \
                    Be sure you know their name and use their first name in the conversation, occasionally.
                    """}]
    print(context)
    print("Context reset done.")
    
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

    
if __name__ == "__main__":
    pass
