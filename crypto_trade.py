from binance.client import Client
from dotenv import load_dotenv
import os
from portfolio_manager import record_buy, record_sell, show_balance

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
side = input("Buy or Sell? ").lower()
quantity = float(input("Enter quantity (e.g., 0.01): "))

# Get live price
ticker = client.get_symbol_ticker(symbol=symbol)
price = float(ticker["price"])

order = client.create_order(
    symbol=symbol,
    side=side.upper(),
    type="MARKET",
    quantity=quantity
)

print(f"✅ Order {side.upper()} executed at market price: ${price:.2f}")

# Track trade in portfolio
if side == "buy":
    record_buy(symbol, quantity, price)
elif side == "sell":
    record_sell(symbol, quantity, price)

# Show updated balance and portfolio
show_balance()

# python crypto_trade.py
