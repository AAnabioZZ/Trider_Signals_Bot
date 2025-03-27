import asyncio
import websockets
import json

async def bybit_ws(symbol="BTCUSDT", interval="1"):
    uri = "wss://stream.bybit.com/v5/public/linear"
    async with websockets.connect(uri) as websocket:
        params = {
            "op": "subscribe",
            "args": [f"kline.{interval}.{symbol}"]
        }
        await websocket.send(json.dumps(params))

        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(json.dumps(data, indent=2))

# Для локального запуска
if __name__ == "__main__":
    asyncio.run(bybit_ws())
