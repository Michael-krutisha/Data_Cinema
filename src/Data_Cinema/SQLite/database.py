import os
import sqlite3

# Находим папку, в которой лежит этот файл database.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Соединяем путь к папке с именем файла базы данных
db_path = os.path.join(BASE_DIR, "database.db")

def get_connection():
    # Вместо старой строки используем db_path
    conn = sqlite3.connect(db_path)
    return conn
