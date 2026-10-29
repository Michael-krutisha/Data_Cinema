# src/database.py
import sqlite3
import os

def get_connection():
    # 1. Находим папку src
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Указываем точный путь к твоей родной заполненной базе данных
    db_path = os.path.join(current_dir, "Data-Cinema", "SQLite", "database.db")
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
