from utils.notifier import send_telegram_message
from trading.trade_engine import execute_trade, get_wallet_status

def handle_command(text: str):
    if text == "/start":
        send_telegram_message("🤖 Bot gestartet.")
    elif text == "/stop":
        send_telegram_message("🛑 Bot gestoppt.")
    elif text == "/wallet":
        wallet = get_wallet_status()
        send_telegram_message(f"💰 Wallet:\n{wallet}")
    elif text == "/buy":
        execute_trade("BTCUSDT", "buy", 0.001)
    elif text == "/sell":
        execute_trade("BTCUSDT", "sell", 0.001)
    else:
        send_telegram_message("❓ Unbekannter Befehl.")
