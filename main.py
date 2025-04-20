# SinanTradingBot_FINAL_v2

# Dies ist die Hauptdatei deines vollautomatischen Trading-Bots
# Sie verbindet Binance, Coinbase und Telegram
# Und führt KI-gesteuerte Trades aus mit Live-Portfolio-Analyse

import os
import time
import threading
from core.binance_engine import BinanceEngine
from core.coinbase_engine import CoinbaseEngine
from core.strategy_ai import StrategyAI
from utils.telegram import notify

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MODE = os.getenv("MODE", "live")

binance = BinanceEngine()
coinbase = CoinbaseEngine()
strategy = StrategyAI()

running = True

def trade_loop():
    while running:
        try:
            portfolio = {
                "binance": binance.get_balances(),
                "coinbase": coinbase.get_balances()
            }

            suggestions = strategy.evaluate(portfolio)

            for suggestion in suggestions:
                platform = suggestion["platform"]
                action = suggestion["action"]
                symbol = suggestion["symbol"]
                amount = suggestion["amount"]

                result = None
                if platform == "binance":
                    result = binance.execute_trade(symbol, action, amount)
                elif platform == "coinbase":
                    result = coinbase.execute_trade(symbol, action, amount)

                if result:
                    notify(f"🟢 Trade auf {platform.upper()}: {action.upper()} {amount} {symbol}\n{result}")
                else:
                    notify(f"🔴 Trade auf {platform.upper()} fehlgeschlagen: {action} {amount} {symbol}")

            time.sleep(60)  # Wartezeit zwischen Zyklen

        except Exception as e:
            notify(f"🚨 Fehler im Trade-Loop: {str(e)}")
            time.sleep(30)

def start():
    notify("🤖 Bot gestartet und live im Modus: " + MODE)
    thread = threading.Thread(target=trade_loop)
    thread.start()

if __name__ == "__main__":
    start()
