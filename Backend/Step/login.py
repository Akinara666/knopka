import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import secrets

# Настройка базы данных и модели
DATABASE_URL = "sqlite:///mydatabase.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class UserLogin(Base):
    __tablename__ = 'user_logins'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Функция проверки логина
def login_user(username, password):
    session = Session()
    user = session.query(UserLogin).filter_by(username=username).first()

    if user:
        # Проверяем, является ли user.password_hash строкой и преобразуем ее в байты, если необходимо
        if isinstance(user.password_hash, str):
            password_hash = user.password_hash.encode()  # преобразуем строку в байты
        else:
            password_hash = user.password_hash  # если уже байты, то просто используем

        if bcrypt.checkpw(password.encode(), password_hash):
            # Если пользователь найден и пароль верен
            token = secrets.token_hex(16)
            print(f"Логин прошел успешно. Ваш временный токен: {token}")
            return token
        else:
            print("Ошибка: неправильный логин или пароль.")
            return None
    else:
        print("Ошибка: пользователь не найден.")
        return None

# Основной код для тестирования функции логина
if __name__ == "__main__":
    # Пример данных для логина
    username = "fred"  # замените на имя пользователя для тестирования
    password = "fred"  # замените на пароль для тестирования

    login_user(username, password)
