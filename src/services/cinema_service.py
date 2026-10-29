# 1 импортируем репозиторие, которые потребуются
# 2 для записи в базу данных, то есть что записано в model
from repositories import Sessions_repository, Tickets_repository, Halls_repository
from database import get_connection

# подключения репозитория с информаццией про фильмы 
def get_available_sessions():
    return Sessions_repository.get_all_with_details()

# проверка на занятость ряда и места( то есть выбранное место пользователя уже куплено или свободно)
def get_taken_seats(session_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT row_number, seat_number FROM Tickets WHERE session_id = ?", (session_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

# проверка на то сколько есть рядом и мест в ряду. есть ли вообще такой сеанс с id 
def check_seat_available(session_id: int, row: int, seat: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT hall_id FROM Sessions WHERE session_id = ?", (session_id,))
    s_row = cur.fetchone()
    if not s_row:
        conn.close()
        return False
        
    hall = Halls_repository.get_by_id(s_row[0])
    if hall and (row > hall.rows_count or row <= 0 or seat > hall.seats_per_row or seat <= 0):
        conn.close()
        return False

    cur.execute("SELECT ticket_id FROM Tickets WHERE session_id = ? AND row_number = ? AND seat_number = ?", (session_id, row, seat))
    res = cur.fetchone()
    conn.close()
    return res is None

# запись забронированного билета(вызываем репозиторий билетов, чтобы записать в базу данных)
def fixate_ticket_sale(session_id: int, user_id: int, row: int, seat: int):
    Tickets_repository.create(session_id, user_id, 450, row, seat, True)
