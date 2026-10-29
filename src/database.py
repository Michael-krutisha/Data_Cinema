# src/database.py
import sqlite3
import os

def get_connection():
    # Находим путь к файлу database.db относительно этого скрипта
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "SQLite", "database.db")
    
    conn = sqlite3.connect(db_path)
    # Включаем поддержку Foreign Key (внешних ключей) для SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
