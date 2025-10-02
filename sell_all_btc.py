from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

# Connect to Binance Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Symbol and asset
symbol = "BTCUSDT"
asset = "BTC"

# Fetch your BTC balance
btc_balance = client.get_asset_balance(asset=asset)
btc_quantity = float(btc_balance['free'])

if btc_quantity > 0:
    print(f"🟡 Selling {btc_quantity} BTC at market price...")
    
    # Place sell order
    order = client.order_market_sell(
        symbol=symbol,
        quantity=round(btc_quantity, 6)
    )
    
    print(f"✅ Sell order placed: {order['executedQty']} BTC")
else:
    print("❌ You have no BTC to sell.")
