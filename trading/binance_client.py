from binance.client import Client

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def place_order(self, symbol, side, quantity):
        order = self.client.create_order(
            symbol=symbol,
            side=side.upper(),  # "BUY" oder "SELL"
            type='MARKET',
            quantity=quantity
        )
        return order

    def get_wallet_balance(self):
        balances = self.client.get_account()["balances"]
        return {b["asset"]: b["free"] for b in balances if float(b["free"]) > 0}
