import sqlite3
import os

# Получаем путь к папке, в которой лежит этот скрипт (то есть к папке SQLite)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def init_db():
    # Собираем точные пути к файлам внутри папки SQLite
    db_path = os.path.join(BASE_DIR, 'database.db')
    schema_path = os.path.join(BASE_DIR, 'schema.sql')
    
    # Подключаемся по точному пути (файл создастся именно в папке SQLite)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Открываем схему по точному пути
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_schema = f.read()
    
    # Выполняем SQL-скрипт для создания таблицы
    cursor.executescript(sql_schema)
    
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена внутри папки SQLite!")

if __name__ == '__main__':
    init_db()
