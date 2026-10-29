from database import get_connection
from models.halls import Hall

def _map(row) -> Hall:
    return Hall(*row)

# Create — Добавление нового зала
def create(name: str, rows_count: int, seats_per_row: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Halls (name, rows_count, seats_per_row) 
        VALUES (?, ?, ?)
    """, (name, rows_count, seats_per_row))
    conn.commit()
    conn.close()

# Read — Получение информации о конкретном зале (нужно для проверки рядов/мест)
def get_by_id(hall_id: int) -> Hall | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT hall_id, name, rows_count, seats_per_row FROM Halls WHERE hall_id = ?", (hall_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
