import os
import PyPDF2
from openai import OpenAI

def speech(text):
    print("OpenAI tts is generating voice output.")
    client = OpenAI()
    speech_file_path = "FridayReplies/speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo", # permitted: 'nova', 'shimmer', 'echo', 'onyx', 'fable', 'alloy'
        input=text
    )
    response.stream_to_file(speech_file_path)

#not being used for now.
def say(text):
    print("OpenAI tts is being called.")
    speech(text)
    # Audio(speech_file_path, autoplay=True, rate=22050)
    os.system("mpg123 speech.mp3")

def write_text_to_file(text, file_path):
    try:
        with open(file_path, 'w') as file:  # Open the file in write mode
            file.write(text)  # Write the text to the file
        print(f"Text written to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")

def read_text_from_file(file_path):
    # Open the PDF file
    pdf_file = open(file_path, 'rb')
    # Read the PDF file
    reader = PyPDF2.PdfReader(pdf_file)
    # Print the number of pages
    print(len(reader.pages))
    # Get the first page
    page = reader.pages[0]
    # Extract the text from the first page
    text = page.extract_text()
    pdf_file.close()
    return text

