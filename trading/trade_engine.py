from trading.binance_client import BinanceClient
import os
from dotenv import load_dotenv
load_dotenv()

client = BinanceClient(
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_API_SECRET"),
    demo_mode=True
)

def execute_trade(symbol: str, side: str, quantity: float):
    return client.place_order(symbol, side, quantity)

def get_wallet_status():
    return client.get_wallet_balance()
