# 1 для хэша(то есть создания пароля, чтобы никто не мог узнать пароль)
# 2 импортируем библиотеку, которая написана в repositories про user 
import hashlib
from repositories import User_repository

# Берет обычный текстовый пароль , превращает его в набор байт и прогоняет через алгоритм SHA-256(хеш)
def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Проверка пароля и логина, если таккой логин или нет. Проверка на пустоту и правильность логина.
def register_user(username: str, password: str, role: str = "client"):
    if not username.strip() or not password.strip():
        raise Exception("Имя пользователя или пароль не могут быть пустыми!")
    
    if User_repository.get_by_username(username.strip()):
        raise Exception("Логин занят")
        
    password_hash = _hash_password(password.strip())
    User_repository.create(username.strip(), password_hash, role)
    
# Проверка на авторизовановасть, берет два хеша и проверяет пароль.
def authenticate(username: str, password: str):
    user = User_repository.get_by_username(username.strip())
    if not user:
        return None
    if user.password_hash == _hash_password(password.strip()):
        return user
    return None
