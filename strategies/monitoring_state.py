import json
import os
from datetime import datetime, timedelta

STATE_FILE = "data/monitoring_state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def should_reanalyze(symbol, now=None, hours_interval=4):
    """
    Возвращает True, если пора провести повторный анализ пары:
    - прошло больше N часов
    """
    now = now or datetime.utcnow()
    state = load_state()

    last_check = state.get(symbol, {}).get("last_check")
    if last_check:
        last_dt = datetime.fromisoformat(last_check)
        if now - last_dt < timedelta(hours=hours_interval):
            return False

    # Обновим состояние
    if symbol not in state:
        state[symbol] = {}
    state[symbol]["last_check"] = now.isoformat()
    save_state(state)
    return True


def update_level_event(symbol, level_type: str, level_value: float):
    """
    Сохраняем событие касания или пробоя уровня
    """
    state = load_state()
    if symbol not in state:
        state[symbol] = {}

    key = f"{level_type}_last"
    state[symbol][key] = level_value
    save_state(state)
