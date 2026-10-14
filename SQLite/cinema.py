import sqlite3
import os
import sys

# Принудительно устанавливаем UTF-8 кодировку вывода для терминала Windows
sys.stdout.reconfigure(encoding='utf-8')

# Автоматически определяем путь к текущей папке скрипта (папка SQLite)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Подключаем файл базы данных в правильной директории
db_path = os.path.join(script_dir, 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Читаем наш спроектированный SQL-скрипт схемы кинотеатра
schema_path = os.path.join(script_dir, 'schema.sql')
with open(schema_path, 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Выполняем создание таблиц и первичное наполнение данными
print("Инициализация базы данных кинотеатра...")
cursor.executescript(sql_script)
conn.commit()
print("Таблицы успешно созданы и наполнены тестовыми данными!\n")

# --- ПРОВЕРКА: Вывод учета результатов продаж (Бизнес-логика из отчета ЛР1) ---
print("=" * 70)
print("ОТЧЕТ АДМИНИСТРАТОРА: ВЫВЕДЕННЫЕ РЕЗУЛЬТАТЫ ПРОДАЖ БИЛЕТОВ")
print("=" * 70)

query = """
SELECT 
    t.ticket_id,
    u.username,
    m.title,
    h.name,
    s.date_time,
    t.row_number,
    t.seat_number,
    s.ticket_price,
    t.payment_status
FROM tickets t
JOIN sessions s ON t.session_id = s.session_id
JOIN users u ON t.user_id = u.user_id
JOIN movies m ON s.movie_id = m.movie_id
JOIN halls h ON s.hall_id = h.hall_id;
"""

cursor.execute(query)
tickets_report = cursor.fetchall()

for row in tickets_report:
    print(f"Билет №{row[0]} | Покупатель: {row[1]}")
    print(f"Фильм: «{row[2]}» | Кинозал: {row[3]}")
    print(f"Дата сеанса: {row[4]} | Место: Ряд {row[5]}, Место {row[6]}")
    print(f"Стоимость: {row[7]} руб. | Статус: {row[8]}")
    print("-" * 70)

# Закрываем соединение
conn.close()