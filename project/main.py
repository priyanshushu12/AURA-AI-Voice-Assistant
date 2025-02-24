from datetime import datetime
from groq import Groq  
import speech_recognition as sr
import Tasks.language_translation
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
from langchain.memory import ConversationBufferMemory
import sys
import os

# API key for Groq API
api_key = key.groq

# Initialize the Groq client
client = Groq(api_key=api_key)

memory = ConversationBufferMemory()

# Initialize the speech recognizer
recognizer = sr.Recognizer()


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    

    # Currency conversion command
    if "convert currency" in user_input_lower:
        print("Entering currency conversion mode.")
        Features.currency_conversion.currency_conversion()  # Call the currency conversion function
        return "Currency conversion completed."
    
    # Check for task-related queries
    if "add task" in user_input_lower:
        print("Entering task addition mode.")
        Tasks.task_manager.add_task()
        return "Task has been added."
    elif "view task" in user_input_lower:
        print("Displaying tasks.")
        Tasks.task_manager.view_tasks()
        return "These are your tasks."
    
    elif "remove task" in user_input_lower:
        print("Entering task removal mode.")
        Tasks.task_manager.remove_task()
        return "Task has been removed."
    
    elif "check due tasks" in user_input_lower:
        print("Checking due tasks.")
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

    # Example handling in `generate_response()` function in main.py
    if "calculate emi" in user_input_lower or "loan emi" in user_input_lower:
        print("Calculating EMI...")
        emi_response = Features.loan_calculator.calculate_emi_from_input()  # This will use the input function for EMI calculation
        return emi_response


    if "translate" in user_input_lower:
        text_to_translate = user_input_lower.replace("translate", "").strip()
        translated_text = Tasks.language_translation.translate_text(text_to_translate, from_lang='en', to_lang='hi')
        return f"Translated text: {translated_text}"

    prompt = f"You are a helpful assistant that can answer any question. {user_input}"

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
        stream=False,
    )
    response = chat_completion.choices[0].message.content
    memory.save_context({"input": user_input}, {"output": response}) 
    return response

# Speak the greeting message once
print("Hello, This is Aura. How may I assist you 😊..")
# Continuous loop to prompt the user
while True:
        user_input = input("Enter your Question: ")
            
        if "search" in user_input or any(browser in user_input for browser in ["chrome", "firefox"]):
                Core.user_access.open_browser_and_search(user_input)
        elif "open" in user_input:
                app_name = user_input.lower().replace("open", "").strip()
                Core.user_access.open_application(app_name)
            
            # Check if the user wants to exit the program
        if "exit" in user_input.lower():
            print("Goodbye! Have a nice day.")
            break

            # Generate a response for user input
        response = generate_response(user_input)
        print(f"Aura: {response}")