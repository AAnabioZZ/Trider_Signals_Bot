import ccxt
import pandas as pd


def fetch_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=100):
    """Загружает исторические данные OHLCV с Bybit"""
    exchange = ccxt.bybit()

    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return None

    # Преобразуем в DataFrame
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df


if __name__ == "__main__":
    df = fetch_ohlcv()
    if df is not None:
        print(df.head())
