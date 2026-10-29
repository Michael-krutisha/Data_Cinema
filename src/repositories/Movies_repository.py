from database import get_connection
from models.movies import Movie

def _map(row) -> Movie:
    return Movie(*row)

# Create — Добавление фильма (Операция для Админа)
def create(title: str, genre: str, duration: int, age_rating: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Movies (title, genre, duration, age_rating) 
        VALUES (?, ?, ?, ?)
    """, (title, genre, duration, age_rating))
    conn.commit()
    conn.close()

# Read — Получение всех фильмов
def get_all() -> list[Movie]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT movie_id, title, genre, duration, age_rating FROM Movies")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

# Delete — Удаление фильма
def delete(movie_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Movies WHERE movie_id = ?", (movie_id,))
    conn.commit()
    conn.close()
