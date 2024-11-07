from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base
from bcrypt import hashpw, gensalt

# Настройка базы данных SQLite
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Базовый класс для определения таблиц
Base = declarative_base()

# Определение таблицы для логинов пользователей
class UserLogin(Base):
    __tablename__ = 'user_logins'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Функция для проверки, занят ли email
def is_email_taken(email: str) -> bool:
    """
    Проверяет, занят ли email.
    """
    return session.query(UserLogin).filter(UserLogin.email == email).first() is not None

# Функция для проверки, занят ли username
def is_username_taken(username: str) -> bool:
    """
    Проверяет, занят ли username.
    """
    return session.query(UserLogin).filter(UserLogin.username == username).first() is not None

# Функция хеширования пароля
def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.
    """
    return hashpw(password.encode(), gensalt()).decode()

# Функция для регистрации пользователя
def register_user(email: str, password: str, username: str):
    """
    Регистрирует нового пользователя.
    """
    if is_email_taken(email):
        raise ValueError("Email уже занят")
    if is_username_taken(username):
        raise ValueError("Имя пользователя уже занято")

    hashed_password = hash_password(password)

    # Создание нового пользователя
    new_user = UserLogin(username=username, password_hash=hashed_password, email=email)

    # Добавление и сохранение в базе данных
    session.add(new_user)
    session.commit()
    print(f"Пользователь {username} успешно зарегистрирован.")

    return {"message": "Пользователь успешно зарегистрирован"}

# Запрашиваем данные пользователя для регистрации
email = input("Введите email: ")
username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")

try:
    result = register_user(email, password, username)
    print(result["message"])
except ValueError as e:
    print(f"Ошибка: {e}")
