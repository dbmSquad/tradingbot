class BinanceClient:
    def __init__(self, api_key, api_secret, demo_mode=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.demo_mode = demo_mode

    def place_order(self, symbol, side, quantity):
        return {"status": "simulated", "symbol": symbol, "side": side, "quantity": quantity}

    def get_wallet_balance(self):
        return {"USDT": 1000, "BTC": 0.01}
