import os
from telegram import Bot
from dotenv import load_dotenv

# Явно указываем путь к .env
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"[signal_sender.py] TELEGRAM_TOKEN: {TELEGRAM_TOKEN}")  # 👈 ОБЯЗАТЕЛЬНО!
print(f"[signal_sender.py] CHAT_ID: {CHAT_ID}")  # 👈 ОБЯЗАТЕЛЬНО!

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal(message: str):
    bot.send_message(chat_id=CHAT_ID, text=message)
