-- Включаем поддержку внешних ключей в SQLite
PRAGMA foreign_keys = ON;

-- Удаляем таблицы, если они существовали (в обратном порядке из-за связей)
DROP TABLE IF EXISTS Tickets;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Halls;
DROP TABLE IF EXISTS Movies;

-- 1. Таблица фильмов
CREATE TABLE Movies (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT,
    duration INTEGER,
    age_rating TEXT
);

-- 2. Таблица залов
CREATE TABLE Halls (
    hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rows_count INTEGER,
    seats_per_row INTEGER
);

-- 3. Таблица пользователей
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT
);

-- 4. Таблица сеансов
CREATE TABLE Sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    hall_id INTEGER,
    date_time TEXT,
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (hall_id) REFERENCES Halls(hall_id) ON DELETE CASCADE
);

-- 5. Таблица билетов
CREATE TABLE Tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    user_id INTEGER,
    ticket_price INTEGER,
    row_number INTEGER,
    seat_number INTEGER,
    payment_status INTEGER DEFAULT 0, -- 0 = false, 1 = true
    FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- ========================================================
-- НАПОЛНЕНИЕ ТАБЛИЦ ДАННЫМИ (ВЫПОЛНИТЕ ЭТОТ БЛОК)
-- ========================================================

-- Заполняем залы (Halls)
INSERT INTO Halls (name, rows_count, seats_per_row) VALUES 
('Красный зал', 10, 12),
('Синий зал IMAX', 15, 20),
('VIP-зал', 5, 6);

-- Заполняем фильмы (Movies)
INSERT INTO Movies (title, genre, duration, age_rating) VALUES 
('Интерстеллар', 'Научная фантастика', 169, '12+'),
('Начало', 'Триллер / Фантастика', 148, '12+'),
('Король Лев', 'Мультфильм', 118, '0+');

-- Заполняем пользователей (User)
INSERT INTO User (username, password_hash, role) VALUES 
('admin', 'hash_protected_123', 'administrator'),
('ivan_ivanov', 'hash_user_qwerty', 'customer'),
('maria_k', 'hash_user_abc', 'customer');

-- Заполняем сеансы (Sessions)
-- Указываем ID созданных фильмов и залов
INSERT INTO Sessions (movie_id, hall_id, date_time) VALUES 
(1, 2, '2026-11-01 18:30'), -- Интерстеллар в Синем зале
(2, 1, '2026-11-01 21:00'), -- Начало в Красном зале
(3, 3, '2026-11-02 12:00'); -- Король Лев в VIP-зале

-- Заполняем билеты (Tickets)
INSERT INTO Tickets (session_id, user_id, ticket_price, row_number, seat_number, payment_status) VALUES 
(1, 2, 450, 5, 8, 1), -- Иван купил билет на Интерстеллар
(1, 3, 450, 5, 9, 0), -- Мария забронировала (не оплачен), место рядом
(2, 2, 350, 3, 4, 1); -- Иван также купил билет на Начало
