import speech_recognition as sr
import pyautogui
import pygetwindow as gw
import pyperclip
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Function for voice command recognition with timeout
def listen():
    """Listen for voice commands and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        print("Listening for command... Speak now.")
        
        try:
            # Wait for user input with a timeout of 3 seconds
            audio = recognizer.listen(source, timeout=3)  
            command = recognizer.recognize_google(audio, language="en-IN")  # Use appropriate language code
            print(f"Command received: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period. Exiting.")
            return "exit"
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Error with the speech service: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error: {e}")
            return ""

# Function to capture and read text from the active window
def read_active_window():
    """Read the content of the currently active window."""
    try:
        # Get the currently active window
        active_window = gw.getActiveWindow()

        if active_window:
            # Bring the active window to the foreground
            active_window.activate()
            pyautogui.sleep(0.5)  # Wait for the window to focus

            # Simulate Ctrl + A (select all text) and Ctrl + C (copy)
            pyautogui.hotkey('ctrl', 'a')  # Select all text
            pyautogui.hotkey('ctrl', 'c')  # Copy selected text
            pyautogui.sleep(1)  # Wait for clipboard content to be copied

            # Get the copied content from the clipboard
            clipboard_content = pyperclip.paste()

            if clipboard_content:
                print(f"Clipboard content:\n{clipboard_content}")  # Debug: Print clipboard content
                speak(clipboard_content)  # Speak the content of the window
            else:
                speak("No text found in the clipboard.")
        else:
            speak("No active window found.")

    except Exception as e:
        speak(f"Error reading the active window: {e}")

# Main loop for listening to commands
if __name__ == "__main__":
    print("Voice Assistant is active. Say 'read window' to read text or 'exit' to quit.")
    while True:
        command = listen()

        if command == "exit":
            speak("Exiting voice assistant mode.")
            break

        elif "read window" in command:
            speak("Reading content from the active window.")
            read_active_window()

        elif command:
            print(f"Unrecognized command: {command}")
