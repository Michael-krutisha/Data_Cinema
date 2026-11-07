from src.Data_Cinema.SQLite.database import get_connection
from models.tickets import Ticket

# Покупка билета для пользевателя
def create(session_id: int, user_id: int, price: int, row: int, seat: int, status: bool):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Tickets (session_id, user_id, ticket_price, row_number, seat_number, payment_status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, user_id, price, row, seat, int(status)))
    conn.commit()
    conn.close()

# Получение билетов конкретного пользователя с деталями сеанса и фильма
def get_by_user(user_id: int) -> list[Ticket]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.ticket_id, t.session_id, t.user_id, t.ticket_price, t.row_number, t.seat_number, t.payment_status, m.title, s.date_time
        FROM Tickets t
        JOIN Sessions s ON t.session_id = s.session_id
        JOIN Movies m ON s.movie_id = m.movie_id
        WHERE t.user_id = ?
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    
    tickets = []
    for r in rows:
        t = Ticket(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6]))
        t.movie_title = r[7]
        t.date_time = r[8]
        tickets.append(t)
    return tickets

# собирает информацию со всех user об их продажи или не продажи билетов
def get_sales_statistics() -> dict:
    conn = get_connection()
    cur = conn.cursor()
    # Считаем общее количество проданных билетов и сумму выручки
    cur.execute("SELECT COUNT(*), SUM(ticket_price) FROM Tickets")
    row = cur.fetchone()
    conn.close()
    
    total_tickets = row[0] if row[0] else 0
    total_revenue = row[1] if row[1] else 0
    
    return {
        "total_tickets": total_tickets,
        "total_revenue": total_revenue
    }

def get_taken_seats(session_id: int) -> list[tuple]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT row_number, seat_number FROM Tickets WHERE session_id = ?", (session_id,))
        return cur.fetchall()

def is_seat_taken(session_id: int, row: int, seat: int) -> bool:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM Tickets WHERE session_id = ? AND row_number = ? AND seat_number = ?",
            (session_id, row, seat)
        )
        return cur.fetchone() is not None
