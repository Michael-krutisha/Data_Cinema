# работа с базой данных sql
# для соединения папок в самой системой
import sqlite3
import os

def get_connection():
    # Нахождение папки src
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Указываем точный путь к заполненной базе данных
    db_path = os.path.join(current_dir, "Data-Cinema", "SQLite", "database.db")
    # для проверки коректности билетов в разные сеансы(которых нет например)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
