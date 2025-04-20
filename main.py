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
from utils.nlp import process_user_input  # NLP-Modul für natürliche Sprache

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MODE = os.getenv("MODE", "live")
TRADE_INTERVAL = int(os.getenv("TRADE_INTERVAL", 60))  # Standard: 60 Sekunden
ERROR_RETRY_INTERVAL = int(os.getenv("ERROR_RETRY_INTERVAL", 30))  # Standard: 30 Sekunden

binance = BinanceEngine()
coinbase = CoinbaseEngine()
strategy = StrategyAI()

running = True
lock = threading.Lock()  # Thread-Sicherheit

def trade_loop():
    global running
    while running:
        with lock:
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

                time.sleep(TRADE_INTERVAL)  # Wartezeit zwischen Zyklen

            except Exception as e:
                notify(f"🚨 Fehler im Trade-Loop: {str(e)}")
                time.sleep(ERROR_RETRY_INTERVAL)

def start_autobot():
    """Startet den Autobot."""
    global running
    running = True
    notify("🤖 Autobot gestartet und live im Modus: " + MODE)
    thread = threading.Thread(target=trade_loop)
    thread.start()

def stop_autobot():
    """Stoppt den Autobot."""
    global running
    running = False
    notify("🤖 Autobot wurde gestoppt.")

def handle_message(user_input):
    """Verarbeitet natürliche Sprache und führt entsprechende Aktionen aus."""
    command = process_user_input(user_input)
    if command == "start_autobot":
        start_autobot()
    elif command == "stop_autobot":
        stop_autobot()
    elif command == "status":
        notify("🤖 Der Bot ist aktuell " + ("aktiv" if running else "gestoppt") + ".")
    else:
        notify("❓ Unbekannter Befehl. Bitte versuchen Sie es erneut.")

def start():
    notify("🤖 Bot gestartet und bereit für Befehle.")
    start_autobot()  # Startet den Autobot automatisch beim Start

if __name__ == "__main__":
    start()
