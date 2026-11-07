from repositories import Sessions_repository, Tickets_repository, Halls_repository

def get_available_sessions():
    """Возвращает список всех сеансов."""
    return Sessions_repository.get_all_with_details()

def get_taken_seats(session_id: int) -> list[tuple]:
    """Возвращает список уже купленных мест для сеанса (работает через репозиторий)."""
    return Tickets_repository.get_taken_seats(session_id)

def check_seat_available(session_id: int, row: int, seat: int) -> bool:
    """Строгая проверка доступности места (бизнес-логика)."""
    # 1. Проверяем, существует ли сеанс
    session = Sessions_repository.get_by_id(session_id)
    if not session:
        return False
        
    # 2. Получаем информацию о зале, чтобы проверить его границы
    hall = Halls_repository.get_by_id(session.hall_id)
    if not hall:
        return False
        
    # Проверка: не выходит ли выбранное место за размеры зала
    if row > hall.rows_count or row <= 0 or seat > hall.seats_per_row or seat <= 0:
        return False
        
    # 3. Проверяем через репозиторий билетов, не занято ли место
    if Tickets_repository.is_seat_taken(session_id, row, seat):
        return False
        
    return True

def fixate_ticket_sale(session_id: int, user_id: int, row: int, seat: int):
    """Оформляет покупку билета через репозиторий билетов."""
    Tickets_repository.create(
        session_id=session_id,
        user_id=user_id,
        price=450,
        row=row,
        seat=seat,
        status=True
    )

