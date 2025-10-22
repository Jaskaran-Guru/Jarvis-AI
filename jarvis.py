# pip install pyttsx3 speechRecognition pyaudio wikipedia-api requests

import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import sys
import random
import requests
from pathlib import Path

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Use female voice if available (more Siri-like)
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)  # Natural speaking rate

# Language settings
user_language = 'en'  # Default English
language_codes = {
    'hindi': 'hi',
    'english': 'en',
    'punjabi': 'pa',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'russian': 'ru',
    'japanese': 'ja',
    'korean': 'ko',
    'chinese': 'zh'
}


def speak(audio):
    """Convert text to speech"""
    print(f"🔵 Assistant: {audio}")
    engine.say(audio)
    engine.runAndWait()


def listen_for_wake_word():
    """Listen for wake word 'hey assistant' or 'hey jarvis'"""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            query = r.recognize_google(audio, language='en-in').lower()
            
            if 'hey assistant' in query or 'hey jarvis' in query or 'hey siri' in query:
                return True
        except:
            pass
    
    return False


def takeCommand():
    """Listen to microphone and return string output"""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return "None"
    
    try:
        print("🔄 Processing...")
        # First try with user's preferred language
        query = r.recognize_google(audio, language=f'{user_language}-IN' if user_language == 'hi' or user_language == 'pa' else user_language)
        print(f"💬 You said: {query}\n")
        return query
        
    except sr.UnknownValueError:
        # Try fallback to English
        try:
            query = r.recognize_google(audio, language='en-IN')
            print(f"💬 You said: {query}\n")
            return query
        except:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return "None"
    except sr.RequestError:
        speak("Sorry, I'm having trouble with the speech service right now")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        return "None"


def translate_text(text, target_lang='en'):
    """Translate text to target language using Google Translate API"""
    try:
        if target_lang == 'en':
            return text
        
        # Using mymemory translation API (free, no key needed)
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            translated = data['responseData']['translatedText']
            return translated
        else:
            return text
    except:
        return text


def get_weather(city=""):
    """Get weather information (requires API key)"""
    # Using wttr.in for simple weather - no API key needed
    try:
        if not city:
            city = "auto"
        response = requests.get(f"http://wttr.in/{city}?format=3", timeout=5)
        if response.status_code == 200:
            weather_info = response.text.strip()
            translated = translate_text(f"The weather is {weather_info}", user_language)
            speak(translated)
        else:
            speak(translate_text("Sorry, I couldn't fetch the weather information", user_language))
    except:
        speak(translate_text("I'm having trouble getting weather information right now", user_language))


def search_web(query):
    """Search on Google"""
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Here's what I found about {query}")


def get_time():
    """Get current time"""
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    speak(f"It's {time_str}")


def get_date():
    """Get current date"""
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    speak(f"Today is {date_str}")


def play_on_youtube(query):
    """Play any video on YouTube"""
    if query:
        # Search and play on YouTube
        search_query = query.replace(" ", "+")
        youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(youtube_url)
        speak(f"Playing {query} on YouTube")
    else:
        # Open YouTube if nothing specific mentioned
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube for you")


def open_application(app_name):
    """Open common applications"""
    apps = {
        'code': 'code',
        'visual studio code': 'code',
        'notepad': 'notepad',
        'calculator': 'calc',
        'paint': 'mspaint',
        'chrome': 'chrome',
        'edge': 'msedge',
        'explorer': 'explorer',
        'file explorer': 'explorer'
    }
    
    if app_name in apps:
        try:
            os.system(apps[app_name])
            speak(f"Opening {app_name}")
        except:
            speak(f"I couldn't open {app_name}")
    else:
        speak(f"I'm not sure how to open {app_name}")


def tell_joke():
    """Tell a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What did one wall say to the other? I'll meet you at the corner!",
        "Why did the math book look sad? Because it had too many problems!"
    ]
    speak(random.choice(jokes))


def set_reminder():
    """Simple reminder feature"""
    speak("What would you like me to remind you about?")
    reminder = takeCommand()
    if reminder != "none":
        speak(f"Okay, I'll remember to remind you about {reminder}. Though I have to admit, I can only remember things during this session!")


def process_command(query):
    """Process user commands with Siri-like responses"""
    global user_language
    query_lower = query.lower()
    
    # Change language command
    if 'change language' in query_lower or 'language change' in query_lower or 'switch language' in query_lower:
        for lang_name, lang_code in language_codes.items():
            if lang_name in query_lower:
                user_language = lang_code
                speak(translate_text(f"Language changed to {lang_name}", user_language))
                return True
        speak(translate_text("Which language would you like? Say Hindi, English, Punjabi, Spanish, French, German, or others", user_language))
        return True
    
    # Greetings
    if any(word in query_lower for word in ['hello', 'hi', 'hey', 'नमस्ते', 'sat sri akal', 'सत श्री अकाल']):
        greetings = [
            "Hello! How can I help you?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to help.",
            "Hello! What's on your mind?"
        ]
        speak(translate_text(random.choice(greetings), user_language))
    
    # How are you
    elif 'how are you' in query_lower or 'कैसे हो' in query_lower or 'कैसी हो' in query_lower:
        responses = [
            "I'm doing great, thanks for asking! How can I help you?",
            "I'm functioning perfectly! What can I do for you today?",
            "All systems operational! How can I assist you?"
        ]
        speak(translate_text(random.choice(responses), user_language))
    
    # Thank you
    elif any(word in query_lower for word in ['thank you', 'thanks', 'धन्यवाद', 'शुक्रिया']):
        responses = [
            "You're welcome!",
            "Happy to help!",
            "Anytime!",
            "My pleasure!"
        ]
        speak(translate_text(random.choice(responses), user_language))
    
    # Weather
    elif 'weather' in query_lower or 'मौसम' in query_lower:
        if 'in' in query_lower:
            city = query_lower.split('in')[-1].strip()
            get_weather(city)
        else:
            get_weather()
    
    # Time
    elif 'time' in query_lower or 'समय' in query_lower:
        get_time()
    
    # Date
    elif 'date' in query_lower or 'today' in query_lower or 'तारीख' in query_lower or 'आज' in query_lower:
        get_date()
    
    # Open websites
    elif 'open youtube' in query_lower or 'youtube खोलो' in query_lower:
        speak(translate_text("Opening YouTube", user_language))
        webbrowser.open("https://youtube.com")
    
    elif 'open google' in query_lower or 'google खोलो' in query_lower:
        speak(translate_text("Opening Google", user_language))
        webbrowser.open("https://google.com")
    
    elif 'open gmail' in query_lower or 'open mail' in query_lower or 'gmail खोलो' in query_lower:
        speak(translate_text("Opening Gmail", user_language))
        webbrowser.open("https://mail.google.com")
    
    elif 'open instagram' in query_lower or 'instagram खोलो' in query_lower:
        speak(translate_text("Opening Instagram", user_language))
        webbrowser.open("https://instagram.com")
    
    elif 'open twitter' in query_lower or 'open x' in query_lower:
        speak(translate_text("Opening Twitter", user_language))
        webbrowser.open("https://twitter.com")
    
    elif 'open facebook' in query_lower or 'facebook खोलो' in query_lower:
        speak(translate_text("Opening Facebook", user_language))
        webbrowser.open("https://facebook.com")
    
    # Search
    elif 'search for' in query_lower or 'search about' in query_lower or 'खोजो' in query_lower or 'सर्च करो' in query_lower:
        search_term = query_lower.replace("search for", "").replace("search about", "").replace("खोजो", "").replace("सर्च करो", "").strip()
        if search_term:
            search_web(search_term)
    
    elif 'google' in query_lower and 'open' not in query_lower:
        search_term = query_lower.replace("google", "").strip()
        if search_term:
            search_web(search_term)
    
    # Wikipedia
    elif 'wikipedia' in query_lower or 'who is' in query_lower or 'what is' in query_lower or 'कौन है' in query_lower or 'क्या है' in query_lower:
        if 'wikipedia' in query_lower:
            search_term = query_lower.replace("wikipedia", "").strip()
        elif 'who is' in query_lower or 'कौन है' in query_lower:
            search_term = query_lower.replace("who is", "").replace("कौन है", "").strip()
        else:
            search_term = query_lower.replace("what is", "").replace("क्या है", "").strip()
        
        if search_term:
            speak(translate_text(f"Searching for {search_term}", user_language))
            search_web(f"wikipedia {search_term}")
    
    # Play anything on YouTube
    elif 'play' in query_lower or 'चलाओ' in query_lower or 'बजाओ' in query_lower:
        # Extract what to play from query
        content = query_lower.replace("play", "").replace("चलाओ", "").replace("बजाओ", "").strip()
        play_on_youtube(content)
    
    # Open applications
    elif 'open' in query_lower or 'खोलो' in query_lower:
        app_name = query_lower.replace("open", "").replace("खोलो", "").strip()
        open_application(app_name)
    
    # Tell a joke
    elif 'joke' in query_lower or 'make me laugh' in query_lower or 'चुटकुला' in query_lower:
        tell_joke()
    
    # Calculator
    elif 'calculate' in query_lower or ('what is' in query_lower and any(op in query_lower for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided'])):
        if any(op in query_lower for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            try:
                # Simple calculation
                calculation = query_lower.replace("calculate", "").replace("what is", "").strip()
                calculation = calculation.replace("plus", "+").replace("minus", "-")
                calculation = calculation.replace("times", "*").replace("divided by", "/")
                result = eval(calculation)
                speak(translate_text(f"The answer is {result}", user_language))
            except:
                speak(translate_text("I couldn't calculate that. Could you try again?", user_language))
    
    # Set reminder
    elif 'remind me' in query_lower or 'reminder' in query_lower or 'याद दिलाना' in query_lower:
        set_reminder()
    
    # Who are you
    elif 'who are you' in query_lower or 'what are you' in query_lower or 'तुम कौन हो' in query_lower or 'आप कौन हो' in query_lower:
        speak(translate_text("I'm your personal voice assistant, inspired by Siri. I'm here to help you with tasks, answer questions, and make your life easier!", user_language))
    
    # What can you do
    elif 'what can you do' in query_lower or 'help' in query_lower or 'your capabilities' in query_lower or 'क्या कर सकते हो' in query_lower:
        speak(translate_text("""I can help you with many things. I can tell you the time and weather, 
               search the web, open websites and applications, play music, tell jokes, 
               do calculations, and much more. Just ask me naturally, like you would ask Siri!""", user_language))
    
    # Exit
    elif any(cmd in query_lower for cmd in ['exit', 'quit', 'goodbye', 'bye', 'stop', 'sleep', 'बंद करो', 'अलविदा']):
        farewells = [
            "Goodbye! Have a great day!",
            "See you later!",
            "Bye! Take care!",
            "Until next time!"
        ]
        speak(translate_text(random.choice(farewells), user_language))
        return False
    
    # Default response
    else:
        responses = [
            "I'm not sure how to help with that. Try asking me something else.",
            "I didn't quite understand that. Could you rephrase?",
            "Hmm, I'm not sure about that one. What else can I help you with?",
            "I don't have an answer for that right now. Try asking something else."
        ]
        speak(translate_text(random.choice(responses), user_language))
    
    return True


def main():
    """Main function with Siri-like wake word activation"""
    print("=" * 60)
    print("🤖 VOICE ASSISTANT - Siri Mode (Multi-Language)")
    print("=" * 60)
    print("💡 Say 'Hey Assistant' or 'Hey Jarvis' to activate")
    print("💡 Speak in ANY language - Hindi, English, Punjabi, etc.")
    print("💡 Say 'Change language to Hindi/Punjabi/etc' to switch")
    print("💡 Or press Ctrl+C to exit\n")
    
    # Initial greeting based on time
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    speak(f"{greeting} I'm ready to assist you. Just say 'Hey Assistant' whenever you need me.")
    
    while True:
        # Listen for wake word
        print("⏸️  Waiting for wake word...")
        
        if listen_for_wake_word():
            # Play activation sound (beep)
            print("✅ Activated!")
            speak(translate_text("Yes?", user_language))
            
            # Take command
            query = takeCommand()
            
            if query != "none":
                # Process the command
                should_continue = process_command(query)
                if not should_continue:
                    break
            
            print()  # Empty line for readability


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        speak("Goodbye!")
        sys.exit()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        speak("Sorry, something went wrong.")
        sys.exit()