import os
import sys

# Добавляем папку src в список путей импорта, чтобы всё работало без ошибок
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.menu import start_app

if __name__ == "__main__":
    start_app()
