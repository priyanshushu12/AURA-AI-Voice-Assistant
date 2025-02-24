# coin.py
import requests

def get_crypto_data(coin_name):
    # CoinGecko API URL to fetch the latest cryptocurrency prices
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=usd"
    
    try:
        response = requests.get(url)
        data = response.json()  # Parse the response JSON
        
        # Check if the response is valid
        if response.status_code == 200:
            if coin_name in data:
                # Extract cryptocurrency price
                price = data[coin_name]['usd']
                
                # Return the formatted price information
                return f"The price of {coin_name.capitalize()} is ${price}"
            else:
                return f"Data for {coin_name} not found."
        else:
            return "Error fetching data."
    
    except Exception as e:
        return f"An error occurred: {e}"
