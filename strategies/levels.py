import pandas as pd


def detect_support_resistance(df: pd.DataFrame, window: int = 5) -> dict:
    """Простое определение уровней поддержки/сопротивления"""
    levels = {'support': [], 'resistance': []}
    for i in range(window, len(df) - window):
        low_range = df['low'][i - window:i + window]
        high_range = df['high'][i - window:i + window]

        support = df['low'][i]
        resistance = df['high'][i]

        if support == min(low_range):
            levels['support'].append((df['timestamp'][i], support))
        if resistance == max(high_range):
            levels['resistance'].append((df['timestamp'][i], resistance))

    return levels


def is_near_level(price: float, levels: list, tolerance: float = 0.005) -> bool:
    """Проверяет, находится ли цена рядом с каким-либо уровнем"""
    for _, level_price in levels:
        if abs(price - level_price) / price < tolerance:
            return True
    return False
