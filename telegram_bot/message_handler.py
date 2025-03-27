from telegram import Update
from telegram.ext import CallbackContext
from utils.data_fetcher import fetch_ohlcv, get_top_symbols, generate_active_pairs_config

import importlib.util
import os
import asyncio


async def test_command(update: Update, context: CallbackContext):
    symbol = "BTC/USDT"
    df = fetch_ohlcv(symbol=symbol, timeframe="1h", limit=2)

    if df is None or df.empty or len(df) < 2:
        await update.message.reply_text("Ошибка при получении данных с Bybit.")
        return

    price_start = df.iloc[0]["close"]
    price_end = df.iloc[1]["close"]
    change = ((price_end - price_start) / price_start) * 100
    arrow = "📈" if change > 0 else "📉"
    text = f"{symbol} {arrow} {change:.2f}% за последний час"

    await update.message.reply_text(text)


def import_active_pairs_module():
    """Динамически подгружает сгенерированный файл active_pairs.py"""
    path = os.path.join(os.path.dirname(__file__), "..", "config", "active_pairs.py")
    spec = importlib.util.spec_from_file_location("active_pairs", path)
    active_pairs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(active_pairs)
    return active_pairs


async def fetch_change(symbol):
    df = fetch_ohlcv(symbol=symbol, timeframe="1h", limit=3)
    if df is None or len(df) < 3:
        return symbol, None
    price_start = df.iloc[0]["close"]
    price_end = df.iloc[2]["close"]
    change = ((price_end - price_start) / price_start) * 100
    return symbol, change


async def list_pairs(update: Update, context: CallbackContext):
    # Обновляем пары
    pairs = get_top_symbols()
    generate_active_pairs_config(pairs)
    active_pairs = import_active_pairs_module()

    # Асинхронно собираем данные
    tasks = []
    for i in range(1, 11):
        symbol = getattr(active_pairs, f"currencyPair{i}", None)
        if symbol:
            tasks.append(fetch_change(symbol))

    results = await asyncio.gather(*tasks)

    # Формируем ответ
    response = "🔍 *Изменение за последние 2 часа:*\n"
    for symbol, change in results:
        if change is None:
            continue
        arrow = "📈" if change > 0 else "📉"
        response += f"{symbol} {arrow} {change:.2f}%\n"

    await update.message.reply_text(response, parse_mode="Markdown")
