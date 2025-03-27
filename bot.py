import subprocess
from telegram_bot.bot import main


# Запускаем основной бот из telegram_bot/bot.py fff
if __name__ == "__main__":
    main()
    subprocess.run(["python", "telegram_bot/bot.py"])