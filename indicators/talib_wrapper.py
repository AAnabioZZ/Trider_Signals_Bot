import talib
import pandas as pd

def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """Вычисляет скользящую среднюю (SMA) для заданного периода."""
    return talib.SMA(series, timeperiod=period)
