from utils.data_fetcher import fetch_ohlcv, get_top_symbols
from config import active_pairs
from strategies.signal_manager import calculate_indicators, check_entry_signal, check_sma_crossover
from strategies.levels import detect_support_resistance, is_near_level
from strategies.monitoring_state import should_reanalyze, update_level_event


def analyze_pair(symbol: str, timeframe: str = "4h") -> dict:
    """
    Анализирует одну пару:
    - проверяет необходимость анализа по времени
    - рассчитывает индикаторы и сигналы
    - оценивает нахождение рядом с уровнем
    - возвращает словарь с результатами
    """

    # Проверка: не запускали ли уже недавно
    if not should_reanalyze(symbol, hours_interval=4):
        return {
            "symbol": symbol,
            "status": "⏳ Пропущено (анализ уже был < 4ч назад)"
        }

    # Получение свечей
    df = fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    if df is None or df.empty or len(df) < 30:
        return {"symbol": symbol, "error": "❌ Недостаточно данных"}

    # Индикаторы
    df = calculate_indicators(df)
    signals = check_entry_signal(df)
    sma_signal = check_sma_crossover(df)

    # Уровни
    levels = detect_support_resistance(df)
    last_price = df["close"].iloc[-1]
    near_level = is_near_level(last_price, levels["support"] + levels["resistance"])

    # Если было касание — можно обновить событие
    if near_level:
        update_level_event(symbol, level_type="touch", level_value=last_price)

    result = {
        "symbol": symbol,
        "trend": signals.get("trend"),
        "rsi": signals.get("rsi"),
        "macd": signals.get("macd_cross"),
        "atr": signals.get("atr"),
        "sma_signal": sma_signal,
        "near_level": near_level,
        "status": "✅ OK"
    }

    return result


def run_strategy_for_all(timeframe: str = "4h") -> list:
    """Запускает анализ для всех активных пар"""
    pairs = [getattr(active_pairs, f"currencyPair{i}") for i in range(1, 11)]
    results = []

    for symbol in pairs:
        data = analyze_pair(symbol, timeframe)
        results.append(data)

    return results
