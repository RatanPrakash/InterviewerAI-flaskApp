import os
import openai
# from openai import OpenAI
from dotenv import load_dotenv


# Get the OpenAI API key from the environment variables
load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=openai_api_key)

# def get_completion(prompt, model="gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0, # this is the degree of randomness of the model's output
#     )
#     return response.choices[0].message["content"]

def get_completion_from_messages(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]

def ask_question(question, context=""):
    prompt = f"Q: {question}\nA:"
    if context:
     context = [{"role": "system",
                "content": """Your name is 'Friday' and you are a helpful 
                    Interviewer chat bot who answers in short and crisp 
                    sentences. Ask beginner level questions on data science and 
                    provide a judgement of the interviewee or the user's answers 
                    correctly. Make sure you ask 3 different questions and get 
                    their answers from the candidate. The 3 questions can be 
                    from these 5 questions - 1. What is machine Learning? 2. 
                    What is reinforcement learning? 3. What is supervised and 
                    unsupervised learning? 4. What is a generative AI? 5. What 
                    is computer Vision? #YOU ONLY COMPLETE SENTENCES AND REPLY 
                    AS ASSISTANT AND DO NOT COMPLETE SENTENCES FOR THE USER. 
                    BEHAVE AS A CONVERSATIONAL CHATBOT AND ONLY ANSWER AS YOUR 
                    ROLE.#"""},
                {"role": "user", "content": f'{context}'},
                {"role": "assistant", "content": f"{prompt}"}]
    
    response = get_completion_from_messages(context)
    ai_answer = response.choices[0].message.content
    return ai_answer

def interview():
    print("Welcome to the Interview Bot!")
    print("I'll ask you a few questions. Please respond naturally.\n")

    questions = [
        "Tell me about yourself.",
        "What are your strengths?",
        "What are your weaknesses?",
        "Why do you want to work for this company?",
        "Can you describe a difficult problem you solved?",
        "Where do you see yourself in 5 years?"
        # Add more questions as needed
    ]

    context = ""
    for question in questions:
        print("Interviewer:", question)
        user_response = input("You: ")
        context += f"{question}\n{user_response}\n"

        bot_response = ask_question(question, context)
        print("Interviewer:", bot_response)

    print("\nThank you for the interview!")

if __name__ == "__main__":
    interview()
