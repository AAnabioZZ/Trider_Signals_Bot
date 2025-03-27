import logging
import os
import sys
from telegram_bot.message_handler import test_command
from telegram_bot.message_handler import list_pairs
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Добавляем корневую папку в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импорты из проекта
from utils.data_fetcher import fetch_ohlcv
from strategies.strategy_manager import check_sma_crossover
from telegram_bot.signal_sender import send_signal

# Загружаем .env
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я трейдинг-бот. Скоро начну искать сигналы!")

async def check_market(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔍 Анализирую рынок...")
    df = fetch_ohlcv()
    signal = check_sma_crossover(df)
    send_signal(signal)
    await update.message.reply_text(f"📊 Результат анализа:\n{signal}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.add_handler(CommandHandler("test", test_command))
    app.add_handler(CommandHandler("list", list_pairs))
    logger.info("Бот запущен ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
