import json
import os

PORTFOLIO_FILE = "portfolio.json"

# Initialize portfolio with your real balance
def init_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        data = {
            "cash": 184956.97120694, 
            "positions": {},
            "pnl": 0
        }
        with open(PORTFOLIO_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Portfolio initialized.")
    else:
        print("⚠️ Portfolio already exists.")

def load_portfolio():
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)

def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=4)

def record_buy(symbol, qty, price):
    portfolio = load_portfolio()
    positions = portfolio["positions"]

    if symbol in positions:
        old_qty = positions[symbol]["qty"]
        old_avg = positions[symbol]["avg_price"]
        new_qty = old_qty + qty
        new_avg = ((old_qty * old_avg) + (qty * price)) / new_qty
    else:
        new_qty = qty
        new_avg = price

    portfolio["cash"] -= qty * price
    positions[symbol] = {"qty": new_qty, "avg_price": new_avg}
    save_portfolio(portfolio)
    print(f"✅ Bought {qty} {symbol} at ${price:.2f}")

def record_sell(symbol, qty, price):
    portfolio = load_portfolio()
    positions = portfolio["positions"]

    if symbol not in positions or positions[symbol]["qty"] < qty:
        print("❌ Not enough to sell")
        return

    avg_price = positions[symbol]["avg_price"]
    pnl = (price - avg_price) * qty
    portfolio["cash"] += qty * price
    portfolio["pnl"] += pnl
    positions[symbol]["qty"] -= qty

    if positions[symbol]["qty"] == 0:
        del positions[symbol]

    save_portfolio(portfolio)
    print(f"✅ Sold {qty} {symbol} at ${price:.2f} | PnL: ${pnl:.2f}")

def show_balance():
    portfolio = load_portfolio()
    print(f"💰 Cash: ${portfolio['cash']:.2f}")
    print(f"📈 Realized PnL: ${portfolio['pnl']:.2f}")
    print("📦 Positions:")
    for symbol, pos in portfolio["positions"].items():
        print(f"  - {symbol}: {pos['qty']} at avg ${pos['avg_price']:.2f}")
