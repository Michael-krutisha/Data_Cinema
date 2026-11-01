# подключение проверки 
# подключения репозитория с билетами 
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
# функция для того, какой путь в терминале будет показываться(например, можно добавить админа, у которого будет совсем другие выборы)

# роли
def role_router(user):
    # Проверяем по имени пользователя
    if user.username == "admin":
        admin_menu(user)
    # Или проверяем по роли из базы данных
    elif hasattr(user, 'role') and user.role == "administrator":
        admin_menu(user)
    else:
        client_menu(user)

# меню админа
def admin_menu(user):
    # Импортируем репозитории для взаимодействия с БД
    import repositories.Movies_repository as movies_repo
    import repositories.Sessions_repository as sessions_repo
    import repositories.Halls_repository as halls_repo
    import repositories.Tickets_repository as tickets_repo

    while True:
        print(f"\n--- Меню Администратора: {user.username if hasattr(user, 'username') else user} ---")
        print("1. Управление фильмами")
        print("2. Управление сеансами")
        print("3. Управление залами")
        print("4. Просмотр учета (Статистика продаж)")
        print("0. Выйти")
        
        choice = input("Действие: ")
        
        # 1. УПРАВЛЕНИЕ ФИЛЬМАМИ
        if choice == "1":
            print("\n--- Управление фильмами ---")
            print("1. Посмотреть список фильмов")
            print("2. Добавить новый фильм")
            print("3. Удалить фильм")
            sub_choice = input("Действие: ")
            
            if sub_choice == "1":
                movies = movies_repo.get_all()
                print("\nСписок доступных фильмов:")
                for m in movies:
                    # m — это объект класса Movie (из твоих моделей)
                    print(f"[{m.movie_id}] {m.title} | Жанр: {m.genre} | {m.duration} мин. | Возраст: {m.age_rating}")
            
            elif sub_choice == "2":
                title = input("Название фильма: ")
                genre = input("Жанр: ")
                duration = int(input("Длительность (мин): "))
                age_rating = input("Возрастной рейтинг (например, 16+): ")
                movies_repo.create(title, genre, duration, age_rating)
                print(f"\n[Успех] Фильм '{title}' добавлен в базу!")
                
            elif sub_choice == "3":
                movie_id = int(input("Введите ID фильма для удаления: "))
                movies_repo.delete(movie_id)
                print(f"\n[Успех] Фильм с ID {movie_id} удален!")

        # 2. УПРАВЛЕНИЕ СЕАНСАМИ
        elif choice == "2":
            print("\n--- Управление сеансами ---")
            print("1. Посмотреть расписание сеансов")
            print("2. Добавить новый сеанс")
            print("3. Удалить сеанс")
            sub_choice = input("Действие: ")
            
            if sub_choice == "1":
                sessions = sessions_repo.get_all_with_details()
                print("\nРасписание сеансов:")
                for s in sessions:
                    print(f"ID сеанса: {s.session_id} | Фильм: {s.movie_title} | Зал: {s.hall_name} | Время: {s.date_time}")
            
            elif sub_choice == "2":
                # Сначала покажем ID фильмов и залов, чтобы админ не угадывал
                print("\nДоступные фильмы (ID):")
                for m in movies_repo.get_all():
                    print(f"  ID {m.movie_id}: {m.title}")
                print("Доступные залы (ID):")
                for h in halls_repo.get_all():
                    print(f"  ID {h.hall_id}: {h.name}")
                
                movie_id = int(input("\nВведите ID фильма: "))
                hall_id = int(input("Введите ID зала: "))
                date_time = input("Введите дату и время (например, 2026-11-01 18:00): ")
                
                sessions_repo.create(movie_id, hall_id, date_time)
                print("\n[Успех] Сеанс успешно добавлен!")
                
            elif sub_choice == "3":
                session_id = int(input("Введите ID сеанса для удаления: "))
                sessions_repo.delete(session_id)
                print(f"\n[Успех] Сеанс №{session_id} успешно отменен.")

        # 3. УПРАВЛЕНИЕ ЗАЛАМИ
        elif choice == "3":
            print("\n--- Управление залами ---")
            print("1. Посмотреть список залов")
            print("2. Сформировать новый зал")
            sub_choice = input("Действие: ")
            
            if sub_choice == "1":
                halls = halls_repo.get_all()
                print("\nСписок залов кинотеатра:")
                for h in halls:
                    print(f"[{h.hall_id}] Зал: {h.name} | Рядов: {h.rows_count} | Мест в ряду: {h.seats_per_row}")
            
            elif sub_choice == "2":
                name = input("Название или номер зала (например, 'Зал 1' или 'VIP'): ")
                rows_count = int(input("Количество рядов: "))
                seats_per_row = int(input("Количество мест в одном ряду: "))
                halls_repo.create(name, rows_count, seats_per_row)
                print(f"\n[Успех] Зал '{name}' успешно сконфигурирован!")

        # 4. ПРОСМОТР УЧЕТА (СТАТИСТИКА)
        elif choice == "4":
            stats = tickets_repo.get_sales_statistics()
            print("\n========================================")
            print("       ОТЧЕТ ПО УЧЕТУ И ПРОДАЖАМ        ")
            print("========================================")
            print(f" Всего проданных билетов: {stats['total_tickets']} шт.")
            print(f" Общая выручка системы:   {stats['total_revenue']} руб.")
            print("========================================")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        # 0. ВЫХОД
        elif choice == "0":
            print("Выход из панели администратора...")
            break
        else:
            print("Ошибка: выбран неверный пункт меню. Попробуйте еще раз.")



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
