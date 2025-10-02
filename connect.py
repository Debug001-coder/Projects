import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load your API keys from the .env file
#   venv\Scripts\activate  
load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Create an Alpaca API object (paper trading)
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

# Test the connection by getting your account info
account = api.get_account()

# Print account status
print("Connected to Alpaca!")
print(f"Account status: {account.status}")
print(f"Buying power: ${account.buying_power}")
