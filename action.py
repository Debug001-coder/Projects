import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load API keys
load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Connect to Alpaca paper trading
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

symbol = input("Stock symbol (e.g., AAPL): ").upper()
side = input("Buy or Sell? ").strip().lower()
qty = int(input("How many shares? "))

# Optional: check for sell eligibility
if side == "sell":
    try:
        position = api.get_position(symbol)
        if int(position.qty) < qty:
            print("❌ You don't have enough shares to sell.")
            exit()
    except:
        print("❌ You don't own this stock.")
        exit()

# Submit order with error handling
try:
    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type='market',
        time_in_force='gtc'
    )
    print(f"✅ {side.capitalize()} order for {qty} shares of {symbol} submitted.")
except Exception as e:
    print(f"❌ Order failed: {e}")


#                 python action.py          venv\Scripts\activate