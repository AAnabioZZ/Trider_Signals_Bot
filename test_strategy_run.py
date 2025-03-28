from strategies.strategy_runner import analyze_pair

symbol = "BTC/USDT"
result = analyze_pair(symbol, timeframe="4h")

print("\n📊 Результат анализа:")
for key, value in result.items():
    print(f"{key}: {value}")
