from src.Data_Cinema.SQLite.database import get_connection
from models.sessions import Session

# Cоединяет таблицу сеансов с таблицами фильмов и залов.
def get_all_with_details() -> list[Session]:
    query = """
        SELECT 
            s.session_id, 
            s.movie_id, 
            s.hall_id, 
            s.date_time, 
            m.title, 
            h.name,
            h.rows_count,
            h.seats_per_row
        FROM Sessions s
        JOIN Movies m ON s.movie_id = m.movie_id
        JOIN Halls h ON s.hall_id = h.hall_id
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        
    sessions = []
    for r in rows:
        # r[:4] — это session_id, movie_id, hall_id, date_time
        # Остальные поля передаем как именованные аргументы
        s = Session(
            *r[:4], 
            movie_title=r[4], 
            hall_name=r[5], 
            rows_count=r[6], 
            seats_per_row=r[7]
        )
        sessions.append(s)
    return sessions


# Позволяет администратору поставить конкретный фильм в конкретный зал на определенное время(то есть поставить новый сеанс).
def create(movie_id: int, hall_id: int, date_time: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Sessions (movie_id, hall_id, date_time) 
        VALUES (?, ?, ?)
    """, (movie_id, hall_id, date_time))
    conn.commit()
    conn.close()
    
# администратору чтобы можно было снять сеанс
def delete(session_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def get_by_id(session_id: int) -> Session | None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT session_id, movie_id, hall_id, date_time FROM Sessions WHERE session_id = ?", (session_id,))
        row = cur.fetchone()
        return Session(*row) if row else None

