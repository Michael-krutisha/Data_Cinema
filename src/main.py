# src/main.py
import os
import sys

if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ИМПОРТИРУЕМ НАШУ ИНИЦИАЛИЗАЦИЮ
from database import init_db
from ui.menu import start_app

if __name__ == "__main__":
    # Вызываем создание таблиц перед стартом меню
    init_db()
    start_app()
