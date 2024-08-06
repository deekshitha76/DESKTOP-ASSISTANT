import os
import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import pyautogui  # pip install pyautogui
import screen_brightness_control as sbc  # pip install screen-brightness-control
import re
import math
import psutil  # pip install psutil
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Chutki. Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"
    return query

def findSong(song_name, music_dir):
    songs = os.listdir(music_dir)
    for song in songs:
        if song_name.lower() in song.lower():
            return os.path.join(music_dir, song)
    return None

def open_whatsapp_web():
    webbrowser.open("https://web.whatsapp.com")

def calculate(expression):
    try:
        expression = re.sub(r'[^0-9+\-*/(). ]', '', expression)
        result = eval(expression, {"__builtins__": None}, {"math": math})
        print(f"The result is {result}")
        speak(f"The result is {result}")
    except Exception as e:
        print(f"Error calculating: {e}")
        speak("Sorry, I could not calculate that.")

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't some couples go to the gym? Because some relationships don't work out.",
        "I would tell you a construction pun, but I'm still working on it."
    ]
    joke = random.choice(jokes)
    print(joke)
    speak(joke)

def shutdown():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

def restart():
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")

def sleep():
    speak("Putting the system to sleep.")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def take_screenshot():
    screenshot = pyautogui.screenshot()
    photos_dir = os.path.join(os.path.expanduser("~"), "Pictures")
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
    screenshot_path = os.path.join(photos_dir, "screenshot.png")
    screenshot.save(screenshot_path)
    speak(f"Screenshot has been taken and saved as screenshot.png in your Photos folder")
    print(f"Screenshot has been taken and saved as screenshot.png in your Photos folder")

def battery_status():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"The system has {percentage} percent battery remaining.")
    print(f"The system has {percentage} percent battery remaining.")

def open_gmail():
    try:
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail.")
    except Exception as e:
        speak("I couldn't open Gmail.")
        print(f"Error opening Gmail: {e}")

def open_folder(folder_name):
    base_dirs = [os.path.expanduser("~"), os.path.join(os.path.expanduser("~"), "Documents"), os.path.join(os.path.expanduser("~"), "Downloads"), os.path.join(os.path.expanduser("~"), "Desktop"), os.path.join(os.path.expanduser("~"), "Pictures"), os.path.join(os.path.expanduser("~"), "Music"), os.path.join(os.path.expanduser("~"), "Videos")]

    folder_found = False
    for base_dir in base_dirs:
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.exists(folder_path):
            os.startfile(folder_path)
            speak(f"Opening {folder_name} folder.")
            folder_found = True
            break

    if not folder_found:
        speak(f"Sorry, I could not find the folder named {folder_name}.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if query == "none":
            continue
        if 'quit' in query:
            speak("Quitting. Goodbye!")
            break
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube and search' in query:
            search_query = query.replace("open youtube and search", "")
            webbrowser.open("http://www.youtube.com/results?search_query=" + search_query)
        elif 'open google and search' in query:
            search_query = query.replace("open google and search", "")
            webbrowser.open("https://www.google.com/search?q=" + search_query)
        elif 'open notepad' in query:
            os.startfile("C:\\Windows\\System32\\notepad.exe")
            speak("What should I write?")
            text_to_write = takeCommand()
            if text_to_write != "none":
                pyautogui.typewrite(text_to_write)
        elif 'play music' in query:
            speak("Which song would you like to play?")
            song_name = takeCommand().lower()
            if song_name != "none":
                music_dir = r"C:\Users\Hp\Desktop\music"
                song_path = findSong(song_name, music_dir)
                if song_path:
                    os.startfile(song_path)
                    speak(f"Playing {song_name}")
                else:
                    speak(f"Sorry, I could not find {song_name} in your music directory.")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"mam, the time is {strTime}")
            print(f"mam, the time is {strTime}")
        elif 'open settings' in query:
            os.system("start ms-settings:")
        elif 'turn up volume' in query:
            pyautogui.press('volumeup')
        elif 'turn down volume' in query:
            pyautogui.press('volumedown')
        elif 'turn up brightness' in query:
            try:
                current_brightness = sbc.get_brightness(display=0)[0]
                sbc.set_brightness(current_brightness + 10, display=0)
                speak(f"Brightness increased to {current_brightness + 10}")
            except Exception as e:
                speak("I couldn't adjust the brightness.")
                print(f"Error adjusting brightness: {e}")
        elif 'turn down brightness' in query:
            try:
                current_brightness = sbc.get_brightness(display=0)[0]
                sbc.set_brightness(current_brightness - 10, display=0)
                speak(f"Brightness decreased to {current_brightness - 10}")
            except Exception as e:
                speak("I couldn't adjust the brightness.")
                print(f"Error adjusting brightness: {e}")
        elif 'open whatsapp' in query:
            open_whatsapp_web()
        elif 'calculate' in query:
            speak("What would you like to calculate?")
            calculation = takeCommand().lower()
            if calculation != "none":
                calculate(calculation)
        elif 'tell me a joke' in query or 'another joke' in query:
            tell_joke()
        elif 'shutdown the system' in query:
            shutdown()
        elif 'restart the system' in query:
            restart()
        elif 'sleep the system' in query:
            sleep()
        elif 'take a screenshot' in query:
            take_screenshot()
        elif 'battery percentage' in query:
            battery_status()
        elif 'open email' in query:
            open_gmail()
        elif 'open folder' in query:
            speak("Which folder would you like to open?")
            folder_name = takeCommand().lower()
            if folder_name != "none":
                open_folder(folder_name)
