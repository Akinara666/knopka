from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Определение базы данных авторизации и модели
DATABASE_URL_AUTH = "sqlite:///users.db"
engine_auth = create_engine(DATABASE_URL_AUTH)
SessionAuth = sessionmaker(bind=engine_auth)
BaseAuth = declarative_base()


# Определение модели AuthorizedUser
class AuthorizedUser(BaseAuth):
    __tablename__ = 'authorized_users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    login_token = Column(String, nullable=False)
    login_time = Column(DateTime, default=datetime.datetime.utcnow)


# Функция для выхода пользователя
def logout_user(token):
    session_auth = SessionAuth()

    # Находим пользователя по токену
    authorized_user = session_auth.query(AuthorizedUser).filter_by(login_token=token).first()

    if authorized_user:
        # Удаляем запись пользователя
        session_auth.delete(authorized_user)
        session_auth.commit()
        print("Выход выполнен успешно. Пользователь удален из базы данных логинов.")
    else:
        print("Ошибка: Токен не найден. Выход невозможен.")

    session_auth.close()


# Основной код для тестирования функции выхода
if __name__ == "__main__":
    # Пример токена для выхода
    token = "d70213a96824ba3a929bb19ac8c61421"  # замените на реальный токен для тестирования
    logout_user(token)
