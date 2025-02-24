import os
import subprocess
import time
import webbrowser
import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("I am listening. Please give a command.")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please try again.")
            return None
        except sr.RequestError:
            speak("Network issue. Please try again later.")
            return None

def open_application(command):
    """
    Opens an application installed on the PC based on the input name.
    """
    app_mapping = {
        "excel": os.path.join(os.environ["PROGRAMFILES"], "Microsoft Office\\root\\Office16\\EXCEL.EXE"),
        "word": os.path.join(os.environ["PROGRAMFILES"], "Microsoft Office\\root\\Office16\\WINWORD.EXE"),
        "notepad": "notepad.exe",
        "chrome": "chrome.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "calculator": "calc.exe",
        "camera": "start microsoft.windows.camera:",  # Camera app
        "file explorer": "explorer.exe",
        "paint": "mspaint.exe",
        "powerpoint": os.path.join(os.environ["PROGRAMFILES"], "Microsoft Office\\root\\Office16\\POWERPNT.EXE"),
        "sql": r"C:\Program Files\MySQL\MySQL Workbench 8.0\MySQLWorkbench.exe",
        "whatsapp": r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2504.2.0_x64__cv1g1gvanyjgm\WhatsApp.exe",
        "outlook": "outlook.exe",
    }

    # Find the app in the command
    app_name = None
    for app in app_mapping.keys():
        if app in command:
            app_name = app
            break

    if app_name in app_mapping:
        app_path = app_mapping[app_name]
        try:
            if app_name == "camera":
                subprocess.run(app_path, shell=True)
            elif app_name == "sql" or app_name == "whatsapp":
                subprocess.run(app_path, shell=True)
            elif app_name == "chrome" and "search" in command:
                search_query = command.split("search", 1)[-1].strip()
                if search_query:
                    url = f"https://www.google.com/search?q={search_query}"
                    webbrowser.get(app_path + " %s").open(url)
            else:
                subprocess.Popen(app_path)
            time.sleep(2)
            speak(f"Opening {app_name}...")
        except FileNotFoundError:
            speak(f"Application '{app_name}' not found on your system.")
        except Exception as e:
            speak(f"Error opening '{app_name}': {e}")
    else:
        speak(f"Sorry, I don't know how to open '{command}'.")

def open_browser_and_search(command):
    """Open the specified browser and search for the query."""
    browser_path = None
    if "chrome" in command:
        browser_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    elif "firefox" in command:
        browser_path = "C:/Program Files/Mozilla Firefox/firefox.exe %s"
    else:
        speak("Defaulting to your system's default browser.")

    if "search" in command:
        search_query = command.split("search", 1)[-1].strip()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            if browser_path:
                webbrowser.get(browser_path).open(url)
            else:
                webbrowser.open(url)
            speak(f"Searching for {search_query}.")
        else:
            speak("I couldn't find a search query in your command.")
    else:
        speak("No search query detected.")

# if __name__ == "__main__":
#     command = listen()
#     if command:
#         if "search" in command or any(browser in command for browser in ["chrome", "firefox", "brave"]):
#             open_browser_and_search(command)
#         else:
#             open_application(command)
