from flask import Flask, request
from bot.telegram_handler import handle_command
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/webhook/telegram", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        text = data["message"].get("text", "")
        handle_command(text)
    return "ok"

@app.route("/")
def home():
    return "🤖 TradingBot läuft!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
