import datetime
import speech_recognition as sr
import os
import pyttsx3
from gtts import gTTS

# def say(text):
#     os.system(f"""say "{text}" """)

# def say(text):
#     # Initialize the text-to-speech engine
#     engine = pyttsx3.init(driverName='nsss')  # Use 'sapi5' on Windows
#     # engine.setProperty('voice', 'com.apple.voice.compact.it-IT.Alice') 
#     engine.setProperty('rate', 200)  # Adjust the speech rate (words per minute)
#     engine.say(text)
#     engine.runAndWait()

def say(text):
    tts = gTTS(text=text, lang='en', slow=False, tld='co.uk')
    tts.save("FridayReplies/output.mp3")
    os.system("mpg123 FridayReplies/output.mp3")
    # os.remove("output.mp3")

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
        musicPath = r"/Users/ratanprakash/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/IIT Techfest 2020  - SHKHR.mp3"
        os.system(f"open '{musicPath}'")
        say("Playing Music.")

def datetime_teller(query):
    if "time right now" in query.lower():
        say(f"the time right now is {datetime.datetime.now().strftime('%H:%M:%S')}")



