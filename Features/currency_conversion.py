import requests
import key
def get_exchange_rate(api_key, from_currency, to_currency):
    """Fetch the exchange rate using the Fixer API."""
    url = f"http://data.fixer.io/api/latest?access_key={api_key}&symbols={from_currency},{to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            rates = data["rates"]
            if from_currency in rates and to_currency in rates:
                return rates[to_currency] / rates[from_currency]
            else:
                return None
    else:
        print("Error fetching data from Fixer API.")
    return None

def currency_conversion():
    """Currency conversion function using text input/output."""
    # Replace with your Fixer API key
    api_key = key.currency
    
    try:
        print("Currency Conversion")
        print("===================")
        amount = float(input("Enter the amount you want to convert: "))
        from_currency = input("Enter the source currency code (e.g., USD): ").upper()
        to_currency = input("Enter the target currency code (e.g., INR): ").upper()

        # Fetch the exchange rate
        rate = get_exchange_rate(api_key, from_currency, to_currency)
        if rate:
            converted_amount = amount * rate
            print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}.")
        else:
            print("Error: Could not retrieve conversion rate. Please check the currency codes and try again.")
    except ValueError:
        print("Invalid input! Please enter numeric values for the amount.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# New function to handle the call from main.py
def convert_currency_via_voice(amount, from_currency, to_currency):
    """Handles currency conversion for the voice assistant."""
    # Replace with your Fixer API key
    api_key = "2ea8e28e557577d27b551728a14b2374"

    try:
        rate = get_exchange_rate(api_key, from_currency, to_currency)
        if rate:
            converted_amount = amount * rate
            result = f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}."
            return result
        else:
            return "Error: Could not retrieve conversion rate. Please check the currency codes and try again."
    except Exception as e:
        return f"An error occurred: {str(e)}"
