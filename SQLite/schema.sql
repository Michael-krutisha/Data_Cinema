
-- =====================================================================
-- 1. СОЗДАНИЕ НЕЗАВИСИМЫХ ТАБЛИЦ (Справочники и Пользователи)
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