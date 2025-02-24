import requests

# Mapping of common stock names to their symbols
stock_name_to_symbol = {
    "tesla": "TSLA",
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "amazon": "AMZN",
    # Add more stock names and their symbols as needed
}

def sanitize_input(user_input):
    """Sanitize user input by removing unnecessary words and normalizing."""
    unnecessary_words = {"for", "the", "of"}  # Add other unnecessary words if needed
    words = user_input.lower().split()
    sanitized_words = [word for word in words if word not in unnecessary_words]
    return " ".join(sanitized_words)

def get_stock_market_data(symbol):
    """Fetch stock market data using Alpha Vantage API."""
    api_key = "CAB2K1GWTHQ4WE3M"  # Replace with your Alpha Vantage API key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Time Series (5min)" in data:
            latest_data = data["Time Series (5min)"]
            latest_time = list(latest_data.keys())[0]
            latest_price = latest_data[latest_time]["4. close"]
            print(f"Stock Update for {symbol}:")
            print(f"Latest Price: {latest_price} USD")
            print(f"Time of Data: {latest_time}")
        else:
            print(f"Error: Could not retrieve stock market data for {symbol}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Aura Listening...")
    print("===================")
    
    while True:
        user_input = input("You said: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        
        # Sanitize input
        sanitized_input = sanitize_input(user_input)
        
        # Convert stock name to symbol
        stock_symbol = stock_name_to_symbol.get(sanitized_input, sanitized_input.upper())
        
        print(f"Fetching stock market data for {stock_symbol}...")
        get_stock_market_data(stock_symbol)
        print("I’m ready to answer, ask anything!")
        print("Aura Listening...")
