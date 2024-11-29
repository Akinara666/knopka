from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

app = Flask(__name__)

# Определение базы данных авторизации и модели
DATABASE_URL_AUTH = "sqlite:///mydatabase.db"
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
    token = "3a43ea67564f19734fd08ab49a999c22"  # замените на реальный токен для тестирования
    logout_user(token)


# Эндпоинт для выхода из аккаунта
@app.route('/logout', methods=['POST'])
def logout():
    # Получаем токен из запроса
    token = request.json.get('token')

    if not token:
        return jsonify({"error": "Токен отсутствует"}), 400

    # Вызываем функцию logout_user
    result = logout_user(token)

    if "error" in result:
        return jsonify(result), 400
    else:
        return jsonify(result), 200


# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True)