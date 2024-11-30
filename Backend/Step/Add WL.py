import datetime
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# База данных для "смотреть позже"
DATABASE_URL_WL = "sqlite:///mydatabase.db"
engine_wl = create_engine(DATABASE_URL_WL)
BaseWl = declarative_base()
SessionWl = sessionmaker(bind=engine_wl)

# База данных пользователей
DATABASE_URL_USERS = "sqlite:///mydatabase.db"
engine_users = create_engine(DATABASE_URL_USERS)
SessionUsers = sessionmaker(bind=engine_users)

class UserWatchLater(BaseWl):
    __tablename__ = 'user_wl'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # Добавленный столбец
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

# Пересоздаем таблицу предпочтений, если база данных очищена
BaseWl.metadata.create_all(engine_wl)

# Проверка наличия пользователя в базе данных `mydatabase.db` и получение его user_id
from sqlalchemy.sql import text

def get_user_id(username: str) -> int:
    session_users = SessionUsers()
    try:
        # Оборачиваем запрос в text()
        query = text("SELECT user_id FROM user_logins WHERE username = :username")
        result = session_users.execute(query, {"username": username}).fetchone()
        return result[0] if result else None  # Возвращаем user_id, если найден
    finally:
        session_users.close()


def add_or_update_wl(username, movie_or_series):
    user_id = get_user_id(username)  # Получаем user_id пользователя
    if not user_id:
        print(f"Ошибка: Пользователь с именем {username} не найден в базе данных пользователей.")
        return

    session = SessionWl()
    try:
        # Проверяем, есть ли уже запись о фильме/сериале для пользователя
        wl = session.query(UserWatchLater).filter_by(user_id=user_id, movie_or_series=movie_or_series).first()
        if wl:
            print(f"Фильм или сериал {movie_or_series} уже добавлен в список 'Смотреть позже'.")
        else:
            new_wl = UserWatchLater(
                user_id=user_id,
                username=username,
                movie_or_series=movie_or_series,
                updated_at=datetime.datetime.now(datetime.timezone.utc)
            )
            session.add(new_wl)
            print(f"Фильм или сериал {movie_or_series} добавлен в список 'Смотреть позже'.")
        session.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def delete_wl(username, movie_or_series):
    user_id = get_user_id(username)
    if not user_id:
        print(f"Ошибка: Пользователь с именем {username} не найден в базе данных пользователей.")
        return

    session = SessionWl()
    try:
        wl = session.query(UserWatchLater).filter_by(user_id=user_id, movie_or_series=movie_or_series).first()
        if wl:
            session.delete(wl)
            session.commit()
            print(f"Фильм или сериал {movie_or_series} удален из списка 'Смотреть позже'.")
        else:
            print(f"Фильм или сериал {movie_or_series} не найден в списке 'Смотреть позже'.")
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def manage_wl():
    action = input(
        "Что вы хотите сделать? \nВведите 'a' для добавления фильма/сериала в список 'Смотреть позже' \nВведите 'd' для удаления \n======>").strip().lower()
    username = input("Введите имя пользователя: ").strip()
    movie_or_series = input("Введите название фильма или сериала: ").strip()

    if action == 'a':
        add_or_update_wl(username, movie_or_series)
    elif action == 'd':
        delete_wl(username, movie_or_series)
    else:
        print("Неверный ввод. Пожалуйста, введите 'a' или 'd'.")

@app.route('/watch-later', methods=['POST'])
def add_to_watch_later_endpoint():
    data = request.json
    username = data.get('username')
    movie_or_series = data.get('movie_or_series')

    if not all([username, movie_or_series]):
        return jsonify({"error": "Укажите username и movie_or_series."}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    result = add_to_watch_later(user_id, username, movie_or_series)
    status_code = 200 if "message" in result else 400
    return jsonify(result), status_code

# Эндпоинт для удаления из "Смотреть позже"
@app.route('/watch-later', methods=['DELETE'])
def delete_from_watch_later_endpoint():
    data = request.json
    username = data.get('username')
    movie_or_series = data.get('movie_or_series')

    if not all([username, movie_or_series]):
        return jsonify({"error": "Укажите username и movie_or_series."}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    result = delete_from_watch_later(user_id, movie_or_series)
    status_code = 200 if "message" in result else 400
    return jsonify(result), status_code

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(debug=True)


# Пример использования
manage_wl()
