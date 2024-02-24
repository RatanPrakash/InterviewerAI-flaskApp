from openai import OpenAI

client = OpenAI(api_key="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")
from functions import *

def write_text_to_file(text, file_path):
    try:
        with open(file_path, 'w') as file:  # Open the file in write mode
            file.write(text)  # Write the text to the file
        print(f"Text written to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")

def InterviewerAI(query, chat):
    print("Interviewer A.I., is now being used.")
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "system",
               "content": """Your name is 'Friday' and you are a helpful Interviewer chat bot who answers in short and crisp sentences. 
               Ask beginner level questions on data science and provide a judgement of the interviewee or the user's answers correctly. 
               Make sure you ask 3 different questions and get their answers from the candidate. The 3 questions can be from these 5 questions -
               1. What is machine Learning? 2. What is reinforcement learning? 3. What is supervised and unsupervised learning? 4. What is a generative AI? 
               5. What is computer Vision?
               #YOU ONLY COMPLETE SENTENCES AND REPLY AS ASSISTANT AND DO NOT COMPLETE SENTENCES FOR THE USER. BEHAVE AS A CONVERSATIONAL CHATBOT AND ONLY ANSWER AS YOUR ROLE.#"""},
              {"role": "user", "content": f'{query}'},
              {"role": "assistant", "content": f"{chat}"}],
    temperature=0.9,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    ai_answer = response.choices[0].message.content
    if "write" in query.lower():
        file_path = f"InterviewExperience/{''.join(query.split('write')[1:])}.txt"
        write_text_to_file(ai_answer, file_path)
        return "Output written to a text file, and saved."
    return ai_answer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    chat = []
    ai_answer = InterviewerAI("this is the beginning of the Interview, greet me as an Interviewer and start my interview.", chat)
    print(ai_answer)
    say(ai_answer)
    chat.append(f"Friday: {ai_answer}")
    while True:
        print(f"CHATS TILL NOW: \n {chat[-2:]} \n")
        print("Friday is listening ...")
        query = speechToText()
        print(f"USER : {query}")

        if "stop listening" in query.lower():
            say("Alright.")
            # write_text_to_file("\n".join(chat), f"InterviewExperience/Interview_{datetime.datetime.now().strftime('%H:%M:%S')}.txt")
            break
        if query:
            ai_answer = InterviewerAI(query, chat)
            print(ai_answer)
            say(ai_answer)
            chat.append(f"User: {query}. \n Friday: {ai_answer}")

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the current date and time as desired for the file name
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')

    # Example usage
    chat = ["This is line 1", "This is line 2", "This is line 3"]
    write_text_to_file("\n".join(chat), f"InterviewExperience/Interview_{formatted_datetime}.txt")

    # write_text_to_file("\n".join(chat),
                       # f"InterviewExperience/Interview_{datetime.datetime.now().strftime('%H:%M:%S')}.txt")