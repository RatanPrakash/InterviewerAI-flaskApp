import datetime
import speech_recognition as sr
import os

# def say(text):
#     os.system(f"""say "{text}" """)


def say(text):
    print("OpenAI tts is being called.")
    from pathlib import Path
    from openai import OpenAI
    from IPython.display import Audio
    client = OpenAI()
    speech_file_path = "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
    )
    response.stream_to_file(speech_file_path)
    # Audio(speech_file_path, autoplay=True, rate=22050)
    os.system("mpg123 speech.mp3")

def speechToText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognising the audio...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except:
            return ""
            # return "Sorry. I couldn't understand that. Can you repeat?"

def write_text_to_file(text, file_path):
    try:
        with open(file_path, 'w') as file:  # Open the file in write mode
            file.write(text)  # Write the text to the file
        print(f"Text written to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")



###############################################################################################################

def site_opener(query):
    if "open" in query.lower():
        import webbrowser
        site_open_query = ''.join(query.split()[1:])
        print(site_open_query)
        webbrowser.open(f"https://{site_open_query}.com")
        say(f"Opening {site_open_query} sir")

#TODO: add app opening functionalities.
def file_opener(query):
    if "play music" in query.lower():
        musicPath = r"/Users/ratanprakash/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album"
        os.system(f"open '{musicPath}'")
        say("Playing Music.")

def datetime_teller(query):
    if "time right now" in query.lower():
        say(f"the time right now is {datetime.datetime.now().strftime('%H:%M:%S')}")



