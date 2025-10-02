import time
import json
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
import pandas as pd

# Load API keys
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Trading settings
symbol = "BTCUSDT"
quantity = 0.5
short_window = 5
long_window = 10
prices = []

# Load or initialize portfolio
portfolio_path = "portfolio.json"
if not os.path.exists(portfolio_path):
    portfolio = {
        "cash": 100000,
        "pnl": 0,
        "positions": {}
    }
    with open(portfolio_path, "w") as f:
        json.dump(portfolio, f, indent=2)
else:
    with open(portfolio_path, "r") as f:
        portfolio = json.load(f)

def get_price_data(symbol):
    klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=long_window + 1)
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    return df

def get_position(symbol):
    return portfolio["positions"].get(symbol, {"qty": 0, "avg_price": 0})

def update_portfolio(qty, side, price, symbol):
    position = get_position(symbol)
    if side == "BUY":
        total_cost = qty * price
        if portfolio["cash"] >= total_cost:
            new_qty = position["qty"] + qty
            avg_price = (
                (position["qty"] * position["avg_price"]) + total_cost
            ) / new_qty if new_qty != 0 else 0

            portfolio["positions"][symbol] = {
                "qty": new_qty,
                "avg_price": avg_price
            }
            portfolio["cash"] -= total_cost

    elif side == "SELL":
        if position["qty"] >= qty:
            portfolio["positions"][symbol]["qty"] -= qty
            portfolio["cash"] += qty * price

            if portfolio["positions"][symbol]["qty"] == 0:
                del portfolio["positions"][symbol]

    with open(portfolio_path, "w") as f:
        json.dump(portfolio, f, indent=2)

def trade():
    df = get_price_data(symbol)
    short_ma = df['close'].rolling(window=short_window).mean().iloc[-1]
    long_ma = df['close'].rolling(window=long_window).mean().iloc[-1]
    current_price = df['close'].iloc[-1]
    position_data = portfolio["positions"].get(symbol, {"qty": 0, "avg_price": 0})
    position_qty = position_data["qty"]
    avg_price = position_data["avg_price"]
    prices.append(current_price)

    print(f"Price: {current_price:.2f} | Short MA: {short_ma:.2f} | Long MA: {long_ma:.2f}")

    if short_ma > long_ma:
       print("🟢 BUY Signal")
       client.order_market_buy(symbol=symbol, quantity=quantity)
       update_portfolio(quantity, "BUY", current_price, symbol)
       print(f"✅ Bought {quantity} BTC at {current_price:.2f}")

    elif short_ma < long_ma and position_qty >= quantity and current_price >= avg_price + 50:
        print("🔴 SELL Signal (Profit condition met)")
        client.order_market_sell(symbol=symbol, quantity=quantity)
        update_portfolio(quantity, "SELL", current_price, symbol)
        print(f"✅ Sold {quantity} BTC at {current_price:.2f}")

    else:
        print("⏸️ Hold")

    return current_price, position_qty


# Start trading loop
while True:
    try:
        current_price, qty = trade()
        print(f"💰 Cash: ${portfolio['cash']:.2f} | 📦 BTC Holdings: {qty} BTC\n")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    time.sleep(30)

