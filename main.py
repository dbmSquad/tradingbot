# SinanTradingBot_FINAL_v2

# Dies ist die Hauptdatei deines vollautomatischen Trading-Bots
# Sie verbindet Binance, Coinbase und Telegram
# Und führt KI-gesteuerte Trades aus mit Live-Portfolio-Analyse

import os
import time
import threading
import logging
import signal
from core.binance_engine import BinanceEngine
from core.coinbase_engine import CoinbaseEngine
from core.strategy_ai import StrategyAI
from utils.telegram import notify
from utils.nlp import process_user_input  # NLP-Modul für natürliche Sprache

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, filename="bot.log", format="%(asctime)s - %(levelname)s - %(message)s")

# Umgebungsvariablen validieren
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID environment variable is not set!")

MODE = os.getenv("MODE", "live")
if MODE not in ["live", "test"]:
    raise ValueError("MODE must be 'live' or 'test'.")

TRADE_INTERVAL = int(os.getenv("TRADE_INTERVAL", 60))  # Standard: 60 Sekunden
ERROR_RETRY_INTERVAL = int(os.getenv("ERROR_RETRY_INTERVAL", 30))  # Standard: 30 Sekunden

# Engines initialisieren
binance = BinanceEngine()
coinbase = CoinbaseEngine()
strategy = StrategyAI()

# Thread-Management
running = True
lock = threading.Lock()
thread = None

def trade_loop():
    global running
    while running:
        with lock:
            try:
                # Portfolio abrufen
                portfolio = {
                    "binance": binance.get_balances(),
                    "coinbase": coinbase.get_balances()
                }
                logging.info(f"Portfolio: {portfolio}")

                # Vorschläge von der Strategie-Engine auswerten
                suggestions = strategy.evaluate(portfolio)

                for suggestion in suggestions:
                    if not all(key in suggestion for key in ["platform", "action", "symbol", "amount"]):
                        logging.warning(f"Ungültiger Vorschlag: {suggestion}")
                        continue

                    platform = suggestion["platform"]
                    action = suggestion["action"]
                    symbol = suggestion["symbol"]
                    amount = suggestion["amount"]

                    result = None
                    if MODE == "test":
                        notify(f"🟡 Testmodus: {action.upper()} {amount} {symbol} auf {platform.upper()} simuliert.")
                    else:
                        if platform == "binance":
                            result = binance.execute_trade(symbol, action, amount)
                        elif platform == "coinbase":
                            result = coinbase.execute_trade(symbol, action, amount)

                        if result:
                            notify(f"🟢 Trade auf {platform.upper()}: {action.upper()} {amount} {symbol}\n{result}")
                        else:
                            notify(f"🔴 Trade auf {platform.upper()} fehlgeschlagen: {action} {amount} {symbol}")

                time.sleep(TRADE_INTERVAL)

            except Exception as e:
                logging.error(f"Fehler im Trade-Loop: {str(e)}")
                notify(f"🚨 Fehler im Trade-Loop: {str(e)}")
                time.sleep(ERROR_RETRY_INTERVAL)

def start_autobot():
    """Startet den Autobot."""
    global running, thread
    running = True
    notify("🤖 Autobot gestartet und live im Modus: " + MODE)
    thread = threading.Thread(target=trade_loop)
    thread.start()

def stop_autobot():
    """Stoppt den Autobot."""
    global running, thread
    running = False
    if thread:
        thread.join()
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

def signal_handler(sig, frame):
    """Signal-Handler für SIGINT (z.B. Strg+C)."""
    stop_autobot()
    notify("🚨 Bot wurde durch SIGINT beendet.")
    exit(0)

def start():
    """Startet den Bot."""
    notify("🤖 Bot gestartet und bereit für Befehle.")
    start_autobot()

# Signal-Handler registrieren
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    start()
