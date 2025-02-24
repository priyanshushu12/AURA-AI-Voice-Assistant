import pyttsx3
from datetime import datetime
from groq import Groq  
import speech_recognition as sr
import Core.user_access
import Utilities.file_manager
import Utilities.power_utilities
import Utilities.system_information
import Tasks.language_translation
import Tasks.task_manager
import Features.media_services
import Features.weather_forecast
import Features.news_updates
import Features.dictionary_tool
import Features.currency_conversion
import Features.country_info
import Features.cryptocurrency_data
import Features.time_management
import Features.emergency_services
import Features.loan_calculator
import Features.stock_market
import Core.install_app
import key
import Tasks.text
from langchain.memory import ConversationBufferMemory
import sys
import os
import Features.whatsapp

# API key for Groq API
api_key = key.groq

# Initialize the Groq client
client = Groq(api_key=api_key)

memory = ConversationBufferMemory()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the voice for the text-to-speech engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
engine.setProperty('rate', 200)  # Adjust the speed of speech
engine.setProperty('volume', 0.9)  # Set volume (0.0 to 1.0)

# Function to speak the output
def speak(text):
    engine.say(text)
    engine.runAndWait()
    

# Function to handle personalized responses
def generate_response(user_input):
    user_input_lower = user_input.lower()

    # Check for specific questions about identity
    if any(keyword in user_input_lower for keyword in ["your name", "who are you","what is your name"]):
        return "I am Aura, your personal assistant, here to help and communicate with you."

    if "meaning of" in user_input.lower() or "synonym of" in user_input.lower() or "antonym of" in user_input.lower() or "spelling of" in user_input.lower():
        response = Features.dictionary_tool.handle_dictionary_input(user_input)
        print(response)
        return response
    

    if "whatsapp" in user_input_lower:
        print("Entering whatsapp massage mode:")
        speak("Entering whatsapp massage mode:")
        Features.whatsapp.send_whatsapp_message()
        return "whatsapp massage mode completely"
    

    # Currency conversion command
    if "convert currency" in user_input_lower:
        print("Entering currency conversion mode.")
        speak("Entering currency conversion mode.")
        Features.currency_conversion.currency_conversion()  # Call the currency conversion function
        return "Currency conversion completed."
        
    
    # Handle the clock-related commands
    if "set alarm" in user_input_lower:
        alarm_date = input("Enter date for alarm (DD-MM-YYYY): ")
        alarm_time = input("Enter time for alarm (HH:MM:SS): ")
        ringtone_path = r"C:\Users\shukla\Desktop\test\new feature\c486-c91f-4044-96ad-19597721794b.mp3"
        Features.time_management.set_alarm(alarm_date, alarm_time, ringtone_path)
        return "Alarm has been set."

    if "start timer" in user_input_lower:
        duration = int(input("Enter duration for timer in seconds: "))
        Features.time_management.start_timer(duration)
        return "Timer started."

    if "start stopwatch" in user_input_lower:
        Features.time_management.stopwatch()
        return "Stopwatch ended."
    
    # Handle app installation command
    if "install app" in user_input_lower:
        app_name = user_input_lower.replace("install app", "").strip()
        if app_name:
            Core.install_app.install_app_from_microsoft_store(app_name)  # Call the install_app function
            return f"Installation process for {app_name} started."
        else:
            return "Please specify the app name to install."
    
    # Check for task-related queries
    if "add task" in user_input_lower:
        print("Entering task addition mode.")
        speak("Entering task addition mode.")
        Tasks.task_manager.add_task()
        return "Task has been added."
    elif "view task" in user_input_lower:
        print("Displaying tasks.")
        speak("Displaying tasks.")
        Tasks.task_manager.view_tasks()
        return "These are your tasks."
    
    elif "remove task" in user_input_lower:
        print("Entering task removal mode.")
        speak("Entering task removal mode.")
        Tasks.task_manager.remove_task()
        return "Task has been removed."
    
    elif "check due tasks" in user_input_lower:
        print("Checking due tasks.")
        speak("Checking due tasks.")
        Tasks.task_manager.check_due_tasks()
        return "These are the due tasks."
    
    # Stock market query
    if "stock price of" in user_input_lower or "stock market" in user_input_lower:
        symbol_start = user_input_lower.find("of") + 3  # Extract symbol after "of"
        symbol = user_input[symbol_start:].strip().upper()
        if symbol:
            print(f"Fetching stock market data for {symbol}...")
            Features.stock_market.get_stock_market_data(symbol)
            return f"Here is the latest stock market update for {symbol}."
        else:
            return "Please specify a valid stock symbol."
    
    # Handle time and date queries
    if "current time" in user_input_lower or "time" in user_input_lower:
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."

    if "current date" in user_input_lower or "date" in user_input_lower:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return f"Today's date is {current_date}."

    # Check if the user asked about the weather
    if "weather" in user_input_lower:
        city_start = user_input_lower.find("of") + 3  # Find the start of the city name after "weather of"
        city_name = user_input[city_start:].strip()
        if city_name:
            # Call the weather function with the city name
            return Features.weather_forecast.get_weather(city_name)

        
     # Check if the user is asking for news
    if "news" in user_input_lower:
        topic_start = user_input_lower.find("about") + 5  # Find the topic after "news about"
        topic = user_input[topic_start:].strip() or "latest news"
        # Fetch news from the news module
        news_articles = Features.news_updates.fetch_current_news_currents(api_key=key.news, query=topic)
        if not news_articles:
            news_articles = Features.news_updates.fetch_recent_news_newsapi(api_key=key.news1, query=topic)
        # Merge and display best news
        Features.news_updates.merge_and_display_best_news(news_articles, news_articles, topic)
        return f"Here are the top news articles about {topic}."
    
     # Check for specific questions about country
    if "country information about" in user_input_lower:
        country_name = user_input_lower.split("country information about")[-1].strip()
        country_info = Features.country_info.get_country_info(country_name)  # Get country info from country.py
        print(country_info)  # Read the country info aloud
        return Features.country_info
    
    
     # Check for specific questions about cryptocurrency
    if "crypto information about" in user_input_lower or "cryptocurrency price of" in user_input_lower:
        coin_name = user_input_lower.split("crypto information about")[-1].strip().split("cryptocurrency price of")[-1].strip()
        crypto_info = Features.cryptocurrency_data.get_crypto_data(coin_name)  # Get cryptocurrency data from coin.py
        print(crypto_info)  # Read the crypto info aloud
        return crypto_info
    
       # Check if the user is asking for emergency numbers
    # Emergency numbers query
    if "emergency numbers for" in user_input_lower:
        country_name = user_input_lower.split("emergency numbers for")[-1].strip()
        emergency_numbers_response = Features.emergency_services.display_emergency_numbers(country_name)  # Get emergency numbers
        print(emergency_numbers_response)  # Read the emergency numbers
        return emergency_numbers_response

    # Check for system info queries
    if "power status" in user_input_lower:
        return Utilities.system_information.check_power_status()
    elif "battery percentage" in user_input_lower:
        return Utilities.system_information.get_battery_percentage()
    elif "disk usage" in user_input_lower:
        return Utilities.system_information.get_disk_usage()
    elif "system uptime" in user_input_lower:
        return Utilities.system_information.get_system_uptime()
    elif "process count" in user_input_lower:
        return Utilities.system_information.get_process_count()
    elif "network status" in user_input_lower:
        return Utilities.system_information.check_network_status()
    elif "active connections" in user_input_lower:
        return Utilities.system_information.get_active_connections()
    elif "available partitions" in user_input_lower:
        return Utilities.system_information.get_available_partitions()
    elif "battery time remaining" in user_input_lower:
        return Utilities.system_information.get_battery_time_remaining()
    elif "user login info" in user_input_lower:
        return Utilities.system_information.get_user_login_info()
    elif "top memory processes" in user_input_lower:
        return Utilities.system_information.get_top_memory_processes()
    
    # Example handling in `generate_response()` function in main.py
    if "calculate emi" in user_input_lower or "loan emi" in user_input_lower:
        print("Calculating EMI...")
        speak("Please provide the loan details.")
        emi_response = Features.loan_calculator.calculate_emi_from_input()  # This will use the input function for EMI calculation
        return emi_response


    if "translate" in user_input_lower:
        text_to_translate = user_input_lower.replace("translate", "").strip()
        translated_text = Tasks.language_translation.translate_text(text_to_translate, from_lang='en', to_lang='hi')
        return f"Translated text: {translated_text}"

    # Default behavior - call the API for other queries

    memory.save_context({"input": user_input}, {"output": "Processing..."})
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="llama3-8b-8192",
        stream=False,
    )
    response = chat_completion.choices[0].message.content
    memory.save_context({"input": user_input}, {"output": response})
    return response

# Speak the greeting message once
print("Hello, This is Aura. How may I assist you?")
speak("Hello, this is Aura. How may I assist you?")

# Flag to determine if it's the first question
first_question = True

# Continuous loop to prompt the user
while True:
    # First question prompt (stays the same)
    if first_question:
        print("Please ask your question (say 'exit' to quit):")
        first_question = False

    # Use the microphone to capture audio
    with sr.Microphone() as source:
        try:
            print("Aura Listening...")
            audio = recognizer.listen(source)

            # Convert speech to text
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")

            # Check for power commands
            for command in Utilities.power_utilities.power_commands:
                if command in user_input.lower():
                    Utilities.power_utilities.execute_power_command(command)

            if "read window" in user_input.lower():
                Tasks.text.speak("Reading content from the active window.") 
                Tasks.text.read_active_window()  
            
            if "search" in user_input or any(browser in user_input for browser in ["chrome", "firefox"]):
                    Core.user_access.open_browser_and_search(user_input)
            elif "open" in user_input:
                    app_name = user_input.lower().replace("open", "").strip()
                    Core.user_access.open_application(app_name)
        

            # Handle play music or video command
            if "play music" in user_input.lower():
                song_name = user_input.lower().replace("play music", "").strip()
                if song_name:
                    Features.media_services.play_music(song_name)  # Call the play_music function from media.py
                else:
                    print("Please specify a song name.")
                
            elif "play video" in user_input.lower():
                video_name = user_input.lower().replace("play video", "").strip()
                if video_name:
                    Features.media_services.play_video(video_name)  # Call the play_video function from media.py
                else:
                    print("Please specify a video name.")
                

            # Handle file/folder operations based on user input
            if "create a file" in user_input.lower():
                file_name = user_input.lower().replace("create a file named", "").strip()
                if file_name:
                    Utilities.file_manager.create_file(file_name)
                else:
                    print("Please specify a file name after 'create a file named'.")
                

            elif "create a folder" in user_input.lower():
                folder_name = user_input.lower().replace("create a folder", "").strip()
                if folder_name:
                    Utilities.file_manager.create_folder(folder_name)
                else:
                    print("Please specify a folder name after 'create a folder'.")
            elif "delete" in user_input.lower():
                item_name = user_input.lower().replace("delete", "").strip()
                Core.file_manager.delete_item(item_name)
                
            elif "rename" in user_input.lower():
                if "to" in user_input.lower():
                    old_name, new_name = user_input.lower().replace("rename", "").split("to")
                    Utilities.file_manager.rename_item(old_name.strip(), new_name.strip())
                else:
                    print("Please specify both old and new names.")

            
            
            # Check if the user wants to exit the program
            if "exit" in user_input.lower():
                print("Goodbye! Have a nice day.")
                speak("Goodbye! Have a nice day.")
                break

            # Generate a response for user input
            response = generate_response(user_input)
            print(f"Aura: {response}")
            speak(response)

        except Exception as e:
            print("Sorry, I did not understand that. Please try again.")
            speak("Sorry, I did not understand that. Please try again.")
            print(f"Error: {e}")

            