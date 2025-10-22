# pip install pyttsx3 speechRecognition pyaudio

import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import sys
from pathlib import Path

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)  # Speed of speech


def speak(audio):
    """Convert text to speech"""
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    """Greet user based on time of day"""
    hour = int(datetime.datetime.now().hour)
    
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am Jarvis Sir. Please tell me how may I help you")


def takeCommand():
    """Listen to microphone and return string output"""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return "None"
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Sorry, there was an error with the speech recognition service")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        return "None"


def search_web(query):
    """Search on Google"""
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Here's what I found for {query}")


def get_time():
    """Get current time"""
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time is {strTime}")


def play_music():
    """Play music from default music directory"""
    music_dir = Path.home() / "Music"
    
    if not music_dir.exists():
        speak("Music directory not found")
        return
    
    songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.flac'))]
    
    if songs:
        print(f"Found {len(songs)} songs")
        os.startfile(os.path.join(music_dir, songs[0]))
        speak("Playing music")
    else:
        speak("No music files found in the music directory")


def open_application(app_name):
    """Open common applications"""
    apps = {
        'code': 'code',  # VS Code
        'notepad': 'notepad',
        'calculator': 'calc',
        'paint': 'mspaint'
    }
    
    if app_name.lower() in apps:
        try:
            os.system(apps[app_name.lower()])
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}")
            print(e)
    else:
        speak(f"I don't know how to open {app_name}")


def main():
    """Main function to run the assistant"""
    wishMe()
    
    while True:
        query = takeCommand().lower()
        
        if query == "none":
            continue
        
        # Exit commands
        if any(cmd in query for cmd in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
            speak("Goodbye Sir! Have a great day!")
            sys.exit()
        
        # Wikipedia search (using web search instead)
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            search_term = query.replace("wikipedia", "").replace("search", "").strip()
            search_web(f"wikipedia {search_term}")
        
        # Open websites
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")
        
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")
        
        elif 'open stackoverflow' in query:
            speak("Opening Stack Overflow")
            webbrowser.open("https://stackoverflow.com")
        
        # Search on Google
        elif 'search' in query or 'google' in query:
            search_term = query.replace("search", "").replace("google", "").replace("for", "").strip()
            if search_term:
                search_web(search_term)
        
        # Play music
        elif 'play music' in query or 'play song' in query:
            play_music()
        
        # Get time
        elif 'time' in query:
            get_time()
        
        # Open applications
        elif 'open' in query:
            app_name = query.replace("open", "").strip()
            open_application(app_name)
        
        # Tell a joke
        elif 'joke' in query:
            speak("Why don't scientists trust atoms? Because they make up everything!")
        
        # Get date
        elif 'date' in query:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {today}")
        
        # Who are you
        elif 'who are you' in query or 'what are you' in query:
            speak("I am Jarvis, your virtual assistant. I'm here to help you with various tasks!")
        
        # Help command
        elif 'help' in query or 'what can you do' in query:
            speak("""I can help you with many things. I can search the web, 
                   open websites like YouTube and Google, tell you the time and date, 
                   play music, open applications, and much more. Just ask me!""")
        
        else:
            speak("I'm not sure how to help with that. Try saying 'help' to see what I can do.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye!")
        sys.exit()
    except Exception as e:
        print(f"Fatal error: {e}")
        speak("Sorry, something went wrong. Shutting down.")
        sys.exit()