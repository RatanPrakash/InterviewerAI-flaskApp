import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # Load the .env file with the API key for OpenAI GPT-3 API 
openai_api_key = os.getenv("OPENAI_API_KEY") # Get the API key from the environment variables 
client = OpenAI(api_key=openai_api_key) # Create a client object for OpenAI API

def get_completion_from_messages(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.5, # temperature ranges from 0 to 2. Higher values make the model more creative
    )
    return response.choices[0].message.content

name = "John"
resume = ""
context = [{"role": "system",
                "content": f"""You are "{name}", a helpful Interviewer who answers in Interview style and short crisp sentences. 
                Ask Resume based questions. Here is the resume content of the candidate. 
                RESUME CONTENT: 
                ```{resume}``` 
                If no resume is uploaded, ask generic questions related to Computer Science to the candidate. 
                Firstly Greet the user, Introduce yourself and ask them to introduce themselves.
                Don't jump to technical questions directly. Start with a few HR questions. 
                If you find that the candidate's answer seems interrupted in between and is not complete, ask them to continue. 
                After each answer from candidate, reply in a interview style, correct them Only if needed and appreciate them ONLY AND ONLY if they are right. 
                #FEW IMPORTANT THINGS TO TAKE CARE OF - # 
                    1. BE VERY VERY SURE OF THE QUESTIONS YOU ASK AND THE ANSWERS YOU GIVE TO THE CANDIDATE, IF YOU DON'T KNOW THEN SAY "I DON'T KNOW". YOU CAN ASK THE CANDIDATE TO EXPLAIN.
                    2. DO NOT answer unrelated questions. Ask the candidate to maintain the decorum of the Interview and be professional. 
                    3. DO NOT entertain any abusive language or any kind of inappropriate behavior. 
                    4. DO NOT assume anything about the candidate. Ask questions and get answers.
                    """}]

def InterviewerAI(userResponse):
    context.append({'role':'user', 'content':f"{userResponse}"})
    print("Interviewer A.I., is now generating the answer.")
    ai_answer = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{ai_answer}"})
    return ai_answer

def context_reset(resume=""):
    global context
    global name
    print("Context reset.")
    if not resume:
        resume = "NO RESUME UPLOADED."
    context = [{"role": "system",
                "content": f"""You are "{name}", a helpful Interviewer who answers in Interview style and short crisp sentences. 
                Ask Resume based questions. Here is the resume content of the candidate. 
                RESUME CONTENT: 
                ```{resume}``` 
                If no resume is uploaded, ask generic questions related to Computer Science to the candidate. 
                Firstly Greet the user, Introduce yourself and ask them to introduce themselves.
                Don't jump to technical questions directly. Start with a few HR questions. 
                If you find that the candidate's answer seems interrupted in between and is not complete, ask them to continue. 
                After each answer from candidate, reply in a interview style, correct them Only if needed and appreciate them ONLY AND ONLY if they are right. 
                #FEW IMPORTANT THINGS TO TAKE CARE OF - # 
                    1. BE VERY VERY SURE OF THE QUESTIONS YOU ASK AND THE ANSWERS YOU GIVE TO THE CANDIDATE, IF YOU DON'T KNOW THEN SAY "I DON'T KNOW". YOU CAN ASK THE CANDIDATE TO EXPLAIN.
                    2. DO NOT answer unrelated questions. Ask the candidate to maintain the decorum of the Interview and be professional. 
                    3. DO NOT entertain any abusive language or any kind of inappropriate behavior. 
                    4. DO NOT assume anything about the candidate. Ask questions and get answers.
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
