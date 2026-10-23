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

-- 4. Таблица сеансов (зависит от Movies и Halls)
CREATE TABLE Sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    hall_id INTEGER,
    date_time TEXT,
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (hall_id) REFERENCES Halls(hall_id) ON DELETE CASCADE
);

-- 5. Таблица билетов (зависит от Sessions и User)
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
