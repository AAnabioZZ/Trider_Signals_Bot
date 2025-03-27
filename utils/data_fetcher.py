import ccxt
import pandas as pd
import os
from dotenv import load_dotenv
from utils.logger import logger

# Загружаем переменные окружения так же, как в telegram_bot/bot.py
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")


def fetch_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=100):
    """Загружает исторические данные OHLCV с Bybit"""

    exchange = ccxt.bybit({
        'apiKey': BYBIT_API_KEY,
        'secret': BYBIT_API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
        }
    })

    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    except Exception as e:
        logger.error(f"[BYBIT] Ошибка загрузки данных: {e}")
        return None

    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df


if __name__ == "__main__":
    df = fetch_ohlcv()
    if df is not None:
        print(df.head())


def get_top_symbols(limit=10):
    """Получает топ-торгуемые пары по объёму"""
    exchange = ccxt.bybit()
    tickers = exchange.fetch_tickers()

    sorted_pairs = sorted(
        tickers.items(),
        key=lambda x: x[1].get('quoteVolume', 0),
        reverse=True
    )

    return [symbol for symbol, _ in sorted_pairs[:limit]]


def generate_active_pairs_config(pairs):
    """Создаёт файл config/active_pairs.py с currencyPair1...10"""
    path = os.path.join(os.path.dirname(__file__), "..", "config", "active_pairs.py")
    with open(path, "w") as f:
        for i, pair in enumerate(pairs, start=1):
            f.write(f'currencyPair{i} = "{pair}"\n')

