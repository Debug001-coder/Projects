import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load your API keys from .env
load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Connect to Alpaca's paper trading API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

# Get all current stock positions
positions = api.list_positions()

# Show portfolio info
if not positions:
    print("🟡 You currently have no open positions.")
else:
    for p in positions:
        print(f"🔹 Symbol: {p.symbol}")
        print(f"   📦 Quantity: {p.qty}")
        print(f"   🎯 Average Buy Price: ${p.avg_entry_price}")
        print(f"   💸 Current Price: ${p.current_price}")
        print(f"   💰 Market Value: ${p.market_value}")
        print(f"   📊 Unrealized PnL: ${p.unrealized_pl}")
        print("-" * 40)
 #                   python portfolio.py