# File Name: pc_task.py
# Contains all the functions and the central command registry for the Desktop Assistant.

import os
import webbrowser
import datetime
import subprocess
import pyautogui
import time
import wikipedia
import requests
import pyttsx3
import speech_recognition as sr
import socket

# =================================================================
# --- Helper Functions ---
# =================================================================

def speak(text):
    """Speaks the given text."""
    try:
        engine = pyttsx3.init('sapi5')
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speech: {e}")

def take_command_from_mic():
    """Listens for a voice command and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        print("Could not understand audio.")
        return "none"

# =================================================================
# --- Task Functions ---
# =================================================================

# Category: Applications
def open_notepad():
    os.startfile("notepad.exe")
    return "Opening Notepad."

def open_calculator():
    subprocess.Popen("calc.exe")
    return "Opening Calculator."

def open_cmd():
    os.system("start cmd")
    return "Opening Command Prompt."

def open_vscode():
    try:
        os.startfile(os.path.expanduser("~\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"))
        return "Opening VS Code."
    except FileNotFoundError:
        return "Error: VS Code not found at the default path."

def open_control_panel():
    os.system("control")
    return "Opening Control Panel."

def open_task_manager():
    os.system("taskmgr")
    return "Opening Task Manager."

# Category: Web Browse
def open_google():
    webbrowser.open("https://google.com")
    return "Opening Google."

def open_youtube():
    webbrowser.open("https://youtube.com")
    return "Opening YouTube."

def open_github():
    webbrowser.open("https://github.com")
    return "Opening GitHub."

def open_stackoverflow():
    webbrowser.open("https://stackoverflow.com")
    return "Opening Stack Overflow."

# Category: Information
def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {now}."

def get_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today}."

def get_weather():
    # Replace 'Jaipur' with your city if needed
    city = "Jaipur"
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        res = requests.get(url)
        return f"The weather in {city} is: {res.text}."
    except Exception:
        return "Sorry, I couldn't fetch the weather."

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Your IP Address is: {ip_address}"
    except Exception:
        return "Could not get the IP address."

# Category: System Control
def take_screenshot():
    timestamp = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot().save(filename)
    return f"Screenshot saved as {filename}."

def shutdown_pc():
    # This will initiate shutdown in 60 seconds. Use 'shutdown /a' to abort.
    os.system("shutdown /s /t 60")
    return "PC will shut down in 60 seconds. To cancel, run 'shutdown /a' in CMD."

def restart_pc():
    # This will initiate restart in 60 seconds.
    os.system("shutdown /r /t 60")
    return "PC will restart in 60 seconds. To cancel, run 'shutdown /a' in CMD."
    
def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "PC locked."

# =================================================================
# --- The Task Registry ---
# =================================================================
# This dictionary holds all information about every command.
# To add a new command:
# 1. Create a function for the task.
# 2. Add a new entry to this dictionary with a unique key.

TASK_REGISTRY = {
    # Applications
    "open_notepad": {"phrases": ["open notepad"], "func": open_notepad, "desc": "Open Notepad", "cat": "Apps"},
    "open_calculator": {"phrases": ["open calculator"], "func": open_calculator, "desc": "Open Calculator", "cat": "Apps"},
    "open_cmd": {"phrases": ["open command prompt", "open cmd"], "func": open_cmd, "desc": "Open Command Prompt", "cat": "Apps"},
    "open_vscode": {"phrases": ["open vs code", "open visual studio code"], "func": open_vscode, "desc": "Open VS Code", "cat": "Apps"},
    "open_control_panel": {"phrases": ["open control panel"], "func": open_control_panel, "desc": "Open Control Panel", "cat": "Apps"},
    "open_task_manager": {"phrases": ["open task manager"], "func": open_task_manager, "desc": "Open Task Manager", "cat": "Apps"},
    # Web Browse
    "open_google": {"phrases": ["open google"], "func": open_google, "desc": "Open Google.com", "cat": "Web"},
    "open_youtube": {"phrases": ["open youtube"], "func": open_youtube, "desc": "Open YouTube.com", "cat": "Web"},
    "open_github": {"phrases": ["open github"], "func": open_github, "desc": "Open GitHub.com", "cat": "Web"},
    "open_stackoverflow": {"phrases": ["open stack overflow"], "func": open_stackoverflow, "desc": "Open Stack Overflow", "cat": "Web"},
    # Information
    "get_time": {"phrases": ["what is the time", "tell me the time"], "func": get_time, "desc": "Tell the current time", "cat": "Info"},
    "get_date": {"phrases": ["what is the date", "tell me today's date"], "func": get_date, "desc": "Tell today's date", "cat": "Info"},
    "get_weather": {"phrases": ["what is the weather", "tell me the weather"], "func": get_weather, "desc": "Get weather for Jaipur", "cat": "Info"},
    "get_ip_address": {"phrases": ["what is my ip address", "tell me my ip"], "func": get_ip_address, "desc": "Get local IP Address", "cat": "Info"},
    # System Control
    "take_screenshot": {"phrases": ["take a screenshot", "capture the screen"], "func": take_screenshot, "desc": "Take a Screenshot", "cat": "System"},
    "shutdown_pc": {"phrases": ["shutdown the pc", "turn off computer"], "func": shutdown_pc, "desc": "Shutdown PC (in 60s)", "cat": "System"},
    "restart_pc": {"phrases": ["restart the pc", "reboot computer"], "func": restart_pc, "desc": "Restart PC (in 60s)", "cat": "System"},
    "lock_pc": {"phrases": ["lock the pc", "lock screen"], "func": lock_pc, "desc": "Lock the PC", "cat": "System"},
}

# =================================================================
# --- Command Executor ---
# =================================================================
def execute_command(query):
    """Finds and executes a command from the registry based on the query."""
    query = query.lower()
    
    # Handle search commands separately
    if "wikipedia" in query:
        search_term = query.replace("wikipedia", "").replace("search", "").strip()
        try:
            summary = wikipedia.summary(search_term, sentences=2)
            return f"According to Wikipedia: {summary}"
        except Exception as e:
            return f"Sorry, I could not find anything on Wikipedia about {search_term}. Error: {e}"

    # Check for direct phrase matches in the registry
    for task_key, task_info in TASK_REGISTRY.items():
        for phrase in task_info["phrases"]:
            if phrase in query:
                result = task_info["func"]()
                speak(result) # Speak the result
                return result

    return "Sorry, I don't know that command."
