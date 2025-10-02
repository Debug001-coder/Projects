import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, secret_key)
client.API_URL = 'https://testnet.binance.vision/api'

# Get current price of BTCUSDT
ticker = client.get_symbol_ticker(symbol="BTCUSDT")
current_price = float(ticker["price"])

# Get account info
account = client.get_account()
balances = account["balances"]

# Check BTC holdings
btc = next(b for b in balances if b["asset"] == "BTC")
btc_qty = float(btc["free"]) + float(btc["locked"])

if btc_qty == 0:
    print("❌ You don't hold any BTC.")
else:
    # Get all filled BTC buy orders
    orders = client.get_all_orders(symbol="BTCUSDT")
    filled_buys = [
        o for o in orders if o["side"] == "BUY" and o["status"] == "FILLED"
    ]

    if not filled_buys:
        print("No filled BTC buy orders found.")
    else:
        # Calculate average buy price
        total_qty = 0
        total_cost = 0

        for order in filled_buys:
            qty = float(order["executedQty"])
            price = float(order["cummulativeQuoteQty"]) / qty
            total_qty += qty
            total_cost += price * qty

        avg_buy_price = total_cost / total_qty if total_qty > 0 else 0
        unrealized_pnl = (current_price - avg_buy_price) * btc_qty

        print(f"🪙 BTC Quantity: {btc_qty:.6f}")
        print(f"💰 Avg Buy Price: ${avg_buy_price:.2f}")
        print(f"📈 Current Price: ${current_price:.2f}")
        print(f"📊 Unrealized PnL: ${unrealized_pnl:.2f}")
#                  python pnl_tracker.py  venv\Scripts\activate
 