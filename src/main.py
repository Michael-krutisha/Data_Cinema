# работа с самим питоном и для вывода русских символов
import os
import sys

# чтобы в терминале выдавал русские символы
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.menu import start_app

if __name__ == "__main__":
    start_app()
