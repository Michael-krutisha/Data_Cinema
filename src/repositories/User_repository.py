from src.Data_Cinema.SQLite.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(*row)

# Регистрация сохранить логин, хэш пароль и роль(покупатель и администратор)
def create(username: str, password_hash: str, role: str = 'client'):
    # Если регистрируется admin(логин), принудительно даем ему роль administrator
    if username == 'admin':
        role = 'administrator'
        
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO User (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()


# Получение пользователя по имени для авторизации (проверка), если такой или нет
def get_by_username(username: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, password_hash, role FROM User WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None