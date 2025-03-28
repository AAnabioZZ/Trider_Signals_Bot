import talib
import numpy as np
import pandas as pd
from indicators.talib_wrapper import calculate_sma


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет в DataFrame все нужные индикаторы:
    - EMA 50 / EMA 200 (определение тренда)
    - RSI (перекупленность / перепроданность)
    - MACD (пересечения для смены тренда)
    - OBV (объём)
    - ATR (волатильность)
    """
    close = df['close'].values.astype(float)
    high = df['high'].values.astype(float)
    low = df['low'].values.astype(float)
    volume = df['volume'].values.astype(float)

    df['ema_50'] = talib.EMA(close, timeperiod=50)
    df['ema_200'] = talib.EMA(close, timeperiod=200)
    df['rsi'] = talib.RSI(close, timeperiod=14)

    macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macd_signal'] = macd_signal
    df['macd_hist'] = macd_hist

    df['obv'] = talib.OBV(close, volume)
    df['atr'] = talib.ATR(high, low, close, timeperiod=14)

    return df


def check_entry_signal(df: pd.DataFrame) -> dict:
    """
    Проверяет сигналы на вход по последней свече:
    - тренд по EMA
    - перекупленность/перепроданность по RSI
    - пересечение MACD
    - значение ATR (волатильность)
    """
    last = df.iloc[-1]
    prev = df.iloc[-2]

    signal = {}

    # Тренд
    if last['ema_50'] > last['ema_200']:
        signal['trend'] = 'long'
    elif last['ema_50'] < last['ema_200']:
        signal['trend'] = 'short'

    # RSI
    if last['rsi'] > 70:
        signal['rsi'] = 'overbought'
    elif last['rsi'] < 30:
        signal['rsi'] = 'oversold'

    # MACD пересечение
    if prev['macd'] < prev['macd_signal'] and last['macd'] > last['macd_signal']:
        signal['macd_cross'] = 'bullish'
    elif prev['macd'] > prev['macd_signal'] and last['macd'] < last['macd_signal']:
        signal['macd_cross'] = 'bearish'

    # ATR
    signal['atr'] = round(last['atr'], 2)

    return signal


def check_sma_crossover(df: pd.DataFrame, short_period=9, long_period=21) -> str:
    """
    Проверка пересечения скользящих средних (SMA):
    - SMA short > SMA long → сигнал на покупку
    - SMA short < SMA long → сигнал на продажу
    """
    df["SMA_Short"] = calculate_sma(df["close"], short_period)
    df["SMA_Long"] = calculate_sma(df["close"], long_period)

    if df["SMA_Short"].iloc[-1] > df["SMA_Long"].iloc[-1]:
        return "🚀 Сигнал на покупку (бычий кроссовер)"
    elif df["SMA_Short"].iloc[-1] < df["SMA_Long"].iloc[-1]:
        return "📉 Сигнал на продажу (медвежий кроссовер)"
    else:
        return "⚖️ Нет чёткого сигнала"
