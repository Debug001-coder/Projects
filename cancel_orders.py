import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()
api = tradeapi.REST(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    base_url='https://paper-api.alpaca.markets'
)

# Cancel all open orders
open_orders = api.list_orders(status='open')
for o in open_orders:
    api.cancel_order(o.id)
    print(f"✅ Canceled order for {o.qty} shares of {o.symbol}")
if not open_orders:
    print("📭 No open orders to cancel.")
#               python cancel_orders.py
