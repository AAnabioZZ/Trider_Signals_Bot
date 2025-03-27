from indicators.talib_wrapper import calculate_sma

def check_sma_crossover(df, short_period=9, long_period=21):
    """Проверяет пересечение скользящих средних и генерирует сигнал"""
    df["SMA_Short"] = calculate_sma(df["close"], short_period)
    df["SMA_Long"] = calculate_sma(df["close"], long_period)

    if df["SMA_Short"].iloc[-1] > df["SMA_Long"].iloc[-1]:
        return "🚀 Сигнал на покупку (бычий кроссовер)"
    elif df["SMA_Short"].iloc[-1] < df["SMA_Long"].iloc[-1]:
        return "📉 Сигнал на продажу (медвежий кроссовер)"
    else:
        return "⚖️ Нет чёткого сигнала"

if __name__ == "__main__":
    import utils.data_fetcher as data_fetcher

    df = data_fetcher.fetch_ohlcv()
    if df is not None:
        print(check_sma_crossover(df))
