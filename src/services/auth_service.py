import hashlib
from repositories import User_repository

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str, role: str = "client"):
    if not username.strip() or not password.strip():
        raise Exception("Имя пользователя или пароль не могут быть пустыми!")
    
    if User_repository.get_by_username(username.strip()):
        raise Exception("Логин занят")
        
    password_hash = _hash_password(password.strip())
    User_repository.create(username.strip(), password_hash, role)

def authenticate(username: str, password: str):
    user = User_repository.get_by_username(username.strip())
    if not user:
        return None
    if user.password_hash == _hash_password(password.strip()):
        return user
    return None
