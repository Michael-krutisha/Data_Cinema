from services import auth_service, cinema_service
from repositories import Tickets_repository

# действия которые будут выполняться в терминале и чтобы после одного действия не выключалась программа
def start_app():
    while True:
        print("\n===== СИСТЕМА DATA-CINEMA =====")
        print("1. Войти в аккаунт")
        print("2. Зарегистрироваться")
        print("0. Выйти из программы")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            user = login_menu()
            if user:
                role_router(user)
        elif choice == "2":
            register_menu()
        elif choice == "0":
            break

# у пользователя спрашиваем логи и пароль, далее сама система проверяет на правильность  
def login_menu():
    print("\n--- Авторизация ---")
    username = input("Логин: ")
    password = input("Пароль: ")
    user = auth_service.authenticate(username, password)
    if user:
        print(f"\nПривет, {user.username}!")
        return user
    print("\nНеверный логин или пароль!")
    return None

# если пользователь занят или неправильный пароль, то возвращает на авторизация и вхождения в систему
def register_menu():
    print("\n--- Регистрация ---")
    while True:
        username = input("Ввод логина: ")
        password = input("Ввод пароля: ")
        try:
            auth_service.register_user(username, password, "client")
            print("\nВывод: регистрация выполнена успешно!")
            break
        except Exception as e:
            print(f"\nСообщение: {e}. Выберите другой.")

def role_router(user):
    client_menu(user)

# если пользователь зашел, то спрашивает посмотреть афишу или посмотреть билеты которые уже куплены. Далее если афиша, то выбор сеанса(какой именно фильм и какой время и какое ограниченние по возрасту)
# далее когда выбрали сеанс, то автоматически переносимся в зал в котором проходи фильм. В нем выбираем ряд и место. Проверка на занятость.
# оплата билета 1 (оплата успшено)
def client_menu(user):
    while True:
        print(f"\n--- Меню Клиента: {user.username} ---")
        print("1. Посмотреть сеансы и купить билет")
        print("2. Мои билеты")
        print("0. Выйти")
        choice = input("Действие: ")
        
        if choice == "1":
            sessions = cinema_service.get_available_sessions()
            for s in sessions:
                print(f"Сеанс №{s.session_id} | Фильм: {s.movie_title} | Время: {s.date_time}")
            
            if not sessions:
                print("Сеансов пока нет.")
                continue
                
            try:
                session_id = int(input("\nВведите ID выбранного сеанса: "))
                while True:
                    taken = cinema_service.get_taken_seats(session_id)
                    print(f"Занятые места (Ряд, Место): {taken}")
                    row = int(input("Введите ряд: "))
                    seat = int(input("Введите место: "))
                    
                    if cinema_service.check_seat_available(session_id, row, seat):
                        break
                    print("\nМесто занято! Возврат к выбору места.")
                
                print(f"\nЗаказ оформлен. СЕАНС №{session_id}, РЯД {row}, МЕСТО {seat}.")
                while True:
                    print("\n--- Оплата билета ---")
                    pay_choice = input("Введите '1' для успешной оплаты или '0' для отмены: ")
                    if pay_choice == "1":
                        from repositories import Tickets_repository
                        Tickets_repository.create(session_id, user.user_id, 450, row, seat, True)
                        print("\nФиксация продажи и выдача электронного билета!")
                        break
                    print("\nОплата не прошла!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            tickets = Tickets_repository.get_by_user(user.user_id)
            for t in tickets:
                print(f"Билет №{t.ticket_id} | Фильм: {t.movie_title} | Ряд {t.row_number}, Место {t.seat_number}")
        elif choice == "0":
            break
