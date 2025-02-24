import requests
import key

# Your WeatherAPI key
api_key = key.api_key

def get_weather(city):
    # WeatherAPI endpoint for current weather
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'

    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Extract relevant weather information
        city_name = data['location']['name']
        country = data['location']['country']
        weather_description = data['current']['condition']['text']
        temperature = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']

        # Return the weather data
        return f"Weather in {city_name}, {country}:\nDescription: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} km/h"
    else:
        return "Error fetching weather data. Please check the city name and API key."
