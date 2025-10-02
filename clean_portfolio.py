import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, secret_key)
client.API_URL = 'https://testnet.binance.vision/api'

# Get account balances
account = client.get_account()
balances = account['balances']

# Sell all coins except BTC
print("🧹 Cleaning Portfolio (Selling all except BTC)...")

for asset in balances:
    symbol = asset['asset']
    free = float(asset['free'])

    if free > 0 and symbol != "BTC":
        try:
            # Try to sell using market order with USDT pair
            trading_pair = f"{symbol}USDT"
            print(f"⚠️ Attempting to sell {free} of {trading_pair}")

            order = client.create_order(
                symbol=trading_pair,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=round(free, 6)  # Binance requires precise rounding
            )
            print(f"✅ Sold {free} {symbol}")
        except Exception as e:
            print(f"❌ Could not sell {symbol}: {e}")

print("✅ Done cleaning. Only BTC should remain.")
