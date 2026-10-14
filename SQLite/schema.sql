-- =====================================================================
-- 1. УДАЛЕНИЕ СТАРЫХ ТАБЛИЦ (в обратном порядке от создания)
-- =====================================================================
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS halls;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;

-- =====================================================================
-- 2. СОЗДАНИЕ НЕЗАВИСИМЫХ ТАБЛИЦ (Справочники и Пользователи)
-- =====================================================================

-- Таблица пользователей (Зрители и Администраторы)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Администратор', 'Зритель')) DEFAULT 'Зритель'
);

-- Таблица кинокартин (Репертуар)
CREATE TABLE movies (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    genre TEXT NOT NULL,
    duration INTEGER NOT NULL, -- Продолжительность в минутах
    age_rating TEXT NOT NULL
);

-- Таблица кинозалов
CREATE TABLE halls (
    hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    rows_count INTEGER NOT NULL,
    seats_per_row INTEGER NOT NULL
);

-- =====================================================================
-- 3. СОЗДАНИЕ ЗАВИСИМЫХ ТАБЛИЦ (Сеансы и Билеты)
-- =====================================================================

-- Таблица расписания сеансов
CREATE TABLE sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    hall_id INTEGER NOT NULL,
    date_time TEXT NOT NULL, -- Дата и время сеанса (ГГГГ-ММ-ДД ЧЧ:ММ)
    ticket_price REAL NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
    FOREIGN KEY (hall_id) REFERENCES halls (hall_id)
);

-- Таблица проданных билетов (Связывает сеанс, место в зале и покупателя)
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    row_number INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    payment_status TEXT NOT NULL CHECK(payment_status IN ('Оплачено', 'Не оплачено')) DEFAULT 'Оплачено',
    UNIQUE(session_id, row_number, seat_number), -- Ограничение: нельзя купить одно место дважды на один сеанс
    FOREIGN KEY (session_id) REFERENCES sessions (session_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- =====================================================================
-- 4. НАПОЛНЕНИЕ ТЕСТОВЫМИ ДАННЫМИ ДЛЯ ДЕМОНСТРАЦИИ
-- =====================================================================

-- Добавляем пользователей разных ролей
INSERT INTO users (username, password, role) VALUES 
    ('admin_kino', 'secure_pass', 'Администратор'),
    ('khaitov_mk', 'password123', 'Зритель');

-- Добавляем фильмы в репертуар
INSERT INTO movies (title, genre, duration, age_rating) VALUES 
    ('Интерстеллар', 'Фантастика', 169, '16+'),
    ('Начало', 'Триллер', 148, '12+');

-- Добавляем кинозалы
INSERT INTO halls (name, rows_count, seats_per_row) VALUES 
    ('Зал 1 (Синий)', 10, 12),
    ('Зал 2 (IMAX)', 15, 20);

-- Формируем расписание сеансов
INSERT INTO sessions (movie_id, hall_id, date_time, ticket_price) VALUES 
    (1, 1, '2026-10-15 15:00', 350.00), -- Интерстеллар в Синем зале
    (2, 2, '2026-10-15 18:30', 500.00); -- Начало в зале IMAX

-- Имитируем успешную фиксацию продажи билета пользователю khaitov_mk (user_id = 2)
INSERT INTO tickets (session_id, user_id, row_number, seat_number, payment_status) VALUES 
    (1, 2, 5, 6, 'Оплачено'); -- Куплен билет на 1-й сеанс, 5 ряд, 6 место
