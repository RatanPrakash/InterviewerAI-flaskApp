import datetime
import speech_recognition as sr
import openai
import os

def say(text):
    os.system(f"""say "{text}" """)

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
        musicPath = r"/Users/ratanprakash/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/IIT Techfest 2020  - SHKHR.mp3"
        os.system(f"open '{musicPath}'")
        say("Playing Music.")

def datetime_teller(query):
    if "time right now" in query.lower():
        say(f"the time right now is {datetime.datetime.now().strftime('%H:%M:%S')}")

