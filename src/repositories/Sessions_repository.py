from database import get_connection
from models.sessions import Session
# Cоединяет таблицу сеансов с таблицами фильмов и залов.
def get_all_with_details() -> list[Session]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.session_id, s.movie_id, s.hall_id, s.date_time, m.title, h.name
        FROM Sessions s
        JOIN Movies m ON s.movie_id = m.movie_id
        JOIN Halls h ON s.hall_id = h.hall_id
    """)
    rows = cur.fetchall()
    conn.close()
    
    sessions = []
    for r in rows:
        s = Session(r[0], r[1], r[2], r[3])
        s.movie_title = r[4]
        s.hall_name = r[5]
        sessions.append(s)
    return sessions
def create(movie_id: int, hall_id: int, date_time: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Sessions (movie_id, hall_id, date_time) 
        VALUES (?, ?, ?)
    """, (movie_id, hall_id, date_time))
    conn.commit()
    conn.close()

def delete(session_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
