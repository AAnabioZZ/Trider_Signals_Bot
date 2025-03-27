import logging

# Создаём глобальный логгер
logger = logging.getLogger("trading_bot")
logger.setLevel(logging.INFO)

# Создаём обработчик и формат
handler = logging.FileHandler("bot.log")  # лог в файл
formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру, если он ещё не добавлен
if not logger.hasHandlers():
    logger.addHandler(handler)
