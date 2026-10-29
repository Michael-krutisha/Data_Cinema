from database import get_connection
from models.tickets import Ticket

# Покупка билета
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
