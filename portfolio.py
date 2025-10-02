import os
from dotenv import load_dotenv
from binance.client import Client

# Load keys
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

# Connect to Binance Testnet
client = Client(api_key, secret_key)
client.API_URL = 'https://testnet.binance.vision/api'

# Get account balances
account = client.get_account()
balances = account['balances']

print("📊 Your Crypto Portfolio:")
for asset in balances:
    free = float(asset['free'])
    locked = float(asset['locked'])
    total = free + locked
    if total > 0:
        print(f"{asset['asset']}: {total}")
# python portfolio.py