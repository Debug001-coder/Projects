from binance.client import Client
import os
from dotenv import load_dotenv
load_dotenv()



client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"))
client.API_URL = 'https://testnet.binance.vision/api'
def get_usdt_balance():
    balances = client.get_account()["balances"]
    for asset in balances:
        if asset["asset"] == "USDT":
            return float(asset["free"])

usdt_balance = get_usdt_balance()
print(f"✅ Your current USDT balance is: ${usdt_balance}")
