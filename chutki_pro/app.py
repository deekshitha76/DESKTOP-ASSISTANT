import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
import pyautogui
import screen_brightness_control as sbc
import re
import math
import psutil
import random
from chutk import open_folder, open_gmail, speak, calculate, wishMe, takeCommand, findSong, tell_joke, shutdown, restart, sleep, take_screenshot, battery_status, open_whatsapp_web
import chutk
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.get_json()
    command = data.get('command', '').lower()
    input_type = data.get('input_type', 'text')

    response = process_input(command)
    
    if input_type == 'voice':
        speak(response)
    return jsonify({"status":"success","response": response})


def process_input(command):
    if 'calculate' in command:
        calc_expression = command.replace('calculate', '').strip()
        result = calculate(calc_expression)
        response = f"The result is {result}"
        return response
    
    elif 'quit' in command:
        speak("Quitting. Goodbye!")
        response = f"success"
        return response
    
    elif 'wikipedia' in command:
        speak('Searching Wikipedia...')
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
        response = results
        return response
    elif 'open youtube and search' in command:
        search_query = command.replace("open youtube and search", "")
        webbrowser.open("http://www.youtube.com/results?search_query=" + search_query)
        response = command
        return response
    elif 'open google and search' in command:
        search_query = command.replace("open google and search", "")
        webbrowser.open("https://www.google.com/search?q=" + search_query)
        response = command
        return response
    elif 'open notepad' in command:
        os.startfile("C:\\Windows\\System32\\notepad.exe")
        speak("What should I write?")
        text_to_write = takeCommand()
        if text_to_write != "none":
            pyautogui.typewrite(text_to_write)
        response = command
        return response
    elif 'play music' in command:
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
        response = command
        return response
    elif 'the time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"mam, the time is {strTime}")
        print(f"mam, the time is {strTime}")

        response = command
        return response
    elif 'open settings' in command:
        os.system("start ms-settings:")
        response = command
        return response
    elif 'turn up volume' in command:
        pyautogui.press('volumeup')
        response = command
        return response
    elif 'turn down volume' in command:
        pyautogui.press('volumedown')
        response = command
        return response
    elif 'turn up brightness' in command:
        try:
            current_brightness = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(current_brightness + 10, display=0)
            speak(f"Brightness increased to {current_brightness + 10}")
        except Exception as e:
            speak("I couldn't adjust the brightness.")
            print(f"Error adjusting brightness: {e}")
        response = command
        return response
    elif 'turn down brightness' in command:
        try:
            current_brightness = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(current_brightness - 10, display=0)
            speak(f"Brightness decreased to {current_brightness - 10}")
        except Exception as e:
            speak("I couldn't adjust the brightness.")
            print(f"Error adjusting brightness: {e}")
        response = command
        return response
    elif 'open whatsapp' in command:
        open_whatsapp_web()
        response = command
        return response
    elif 'calculate' in command:
        speak("What would you like to calculate?")
        calculation = takeCommand().lower()
        if calculation != "none":
            calculate(calculation)
        response = command
        return response
    elif 'tell me a joke' in command or 'another joke' in command:
        tell_joke()
        response = command
        return response
    elif 'shutdown the system' in command:
        shutdown()
        response = command
        return response
    elif 'restart the system' in command:
        restart()
        response = command
        return response
    elif 'sleep the system' in command:
        sleep()
        response = command
        return response
    elif 'take a screenshot' in command:
        take_screenshot()
        response = command
        return response
    elif 'battery percentage' in command:
        battery_status()
        response = command
        return response
    elif 'open email' in command:
        open_gmail()
        response = command
        return response
    elif 'open folder' in command:
        speak("Which folder would you like to open?")
        folder_name = takeCommand().lower()
        if folder_name != "none":
            open_folder(folder_name)
        response = command
        return response

    elif 'search' in command:
        search_query = command.replace('search', '').strip()
        results = wikipedia.summary(search_query, sentences=2)
        response = results
        return response




    
    
    else:
        response = f"Command received: {command}"

    return response

if __name__ == '__main__':
    wishMe()
    app.run(debug=True)
