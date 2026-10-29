# src/database.py
import sqlite3
import os

def get_connection():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "SQLite", "database.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Создает все таблицы базы данных, если они еще не существуют"""
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Таблица фильмов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        duration INTEGER NOT NULL,
        age_rating TEXT NOT NULL
    );
    """)
    
    # 2. Таблица залов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Halls (
        hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rows_count INTEGER NOT NULL,
        seats_per_row INTEGER NOT NULL
    );
    """)
    
    # 3. Таблица пользователей
    cur.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """)
    
    # 4. Таблица сеансов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        hall_id INTEGER NOT NULL,
        date_time TEXT NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
        FOREIGN KEY (hall_id) REFERENCES Halls(hall_id) ON DELETE CASCADE
    );
    """)
    
    # 5. Таблица билетов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        ticket_price INTEGER NOT NULL,
        row_number INTEGER NOT NULL,
        seat_number INTEGER NOT NULL,
        payment_status INTEGER NOT NULL,
        FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
    );
    """)
    
    # Добавим тестовый фильм и зал, если база пустая, чтобы было что тестировать
    cur.execute("SELECT COUNT(*) FROM Movies")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO Movies (title, genre, duration, age_rating) VALUES ('Интерстеллар', 'Фантастика', 169, '12+')")
        cur.execute("INSERT INTO Halls (name, rows_count, seats_per_row) VALUES ('Зал 1 Люкс', 5, 10)")
        cur.execute("INSERT INTO Sessions (movie_id, hall_id, date_time) VALUES (1, 1, '29.10.2026 18:00')")
        
    conn.commit()
    conn.close()
