import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Connect to Alpaca paper trading
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

# Fetch recent orders
orders = api.list_orders(status='all', limit=10)

if not orders:
    print("📭 No recent orders found.")
else:
    print("📋 Recent Orders:")
    for order in orders:
        print(f"🔹 Symbol: {order.symbol}")
        print(f"   🛒 Side: {order.side}")
        print(f"   📦 Qty: {order.qty}")
        print(f"   🕒 Submitted at: {order.submitted_at}")
        print(f"   📌 Status: {order.status}")
        print(f"   🔗 ID: {order.id}")
        print("-" * 40)
 #                 python orders.py
