# Dictionary of emergency service numbers based on country
emergency_numbers = {
    "India": {
        "Police": "100" or "112",
        "Fire": "101",
        "Ambulance": "102",
        "Disaster Management": "108",
        "Electricity Complaint": "1912",
        "Women Helpline": "1090",
    },
    "USA": {
        "Police": "911",
        "Fire": "911",
        "Ambulance": "911",
        "Poison Control": "1-800-222-1222"
    },
    "UK": {
        "Police": "999",
        "Fire": "999",
        "Ambulance": "999",
        "NHS Direct": "111"
    },
    # Add more countries as needed
}

# Function to get emergency numbers based on the country
def get_emergency_numbers(country):
    country = country.capitalize()  # Capitalize to handle user input case
    if country in emergency_numbers:
        return emergency_numbers[country]
    else:
        return "Sorry, emergency numbers for this country are not available."

# Function to display the emergency numbers
def display_emergency_numbers(country):
    emergency_info = get_emergency_numbers(country)
    if isinstance(emergency_info, dict):
        response = f"Emergency Numbers for {country}:\n"
        for service, number in emergency_info.items():
            response += f"{service}: {number}\n"
        return response
    else:
        return emergency_info
