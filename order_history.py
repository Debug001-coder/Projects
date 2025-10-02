from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, api_secret, testnet=True)

symbol = "BTCUSDT"

# Get all trades (completed orders)
trades = client.get_my_trades(symbol=symbol)

total_profit = 0

for trade in trades:
    print(f"Symbol: {trade['symbol']}")
    print(f"Side: {'BUY' if trade['isBuyer'] else 'SELL'}")
    print(f"Price: {trade['price']}")
    print(f"Qty: {trade['qty']}")
    print(f"Commission: {trade['commission']} {trade['commissionAsset']}")
    print(f"Time: {trade['time']}")
    print("-" * 30)

#                python order_history.py
