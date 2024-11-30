import datetime
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text

app = Flask(__name__)

# База данных для предпочтений
DATABASE_URL_PREFS = "sqlite:///mydatabase.db"
engine_prefs = create_engine(DATABASE_URL_PREFS)
BasePrefs = declarative_base()
SessionPrefs = sessionmaker(bind=engine_prefs)

# База данных пользователей
DATABASE_URL_USERS = "sqlite:///mydatabase.db"
engine_users = create_engine(DATABASE_URL_USERS)
SessionUsers = sessionmaker(bind=engine_users)

class UserPreference(BasePrefs):
    __tablename__ = 'user_preferences'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # Добавленный столбец
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc),
                        onupdate=datetime.datetime.now(datetime.timezone.utc))


# Пересоздаем таблицу предпочтений, если база данных очищена
BasePrefs.metadata.create_all(engine_prefs)

# Проверка наличия пользователя в базе данных `mydatabase.db` и получение его user_id
def get_user_id(username: str) -> int:
    session_users = SessionUsers()
    try:
        # Изменяем запрос, чтобы получать user_id
        query = text("SELECT user_id FROM user_logins WHERE username = :username")
        result = session_users.execute(query, {"username": username}).first()
        return result[0] if result else None  # Возвращаем user_id, если найден
    finally:
        session_users.close()

def add_or_update_preference(username, movie_or_series, rating):
    user_id = get_user_id(username)  # Получаем user_id пользователя
    if not user_id:
        print(f"Ошибка: Пользователь с именем {username} не найден в базе данных пользователей.")
        return

    session = SessionPrefs()
    try:
        preference = session.query(UserPreference).filter_by(user_id=user_id, movie_or_series=movie_or_series).first()
        if preference:
            preference.rating = rating
            preference.updated_at = datetime.datetime.now(datetime.timezone.utc)
            print(f"Оценка для {movie_or_series} обновлена на {rating}.")
        else:
            new_preference = UserPreference(
                user_id=user_id,  # Сохраняем user_id пользователя
                username=username,
                movie_or_series=movie_or_series,
                rating=rating,
                updated_at=datetime.datetime.now(datetime.timezone.utc)
            )
            session.add(new_preference)
            print(f"Оценка для {movie_or_series} добавлена.")
        session.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def delete_preference(username, movie_or_series):
    user_id = get_user_id(username)
    if not user_id:
        print(f"Ошибка: Пользователь с именем {username} не найден в базе данных пользователей.")
        return

    session = SessionPrefs()
    try:
        preference = session.query(UserPreference).filter_by(user_id=user_id, movie_or_series=movie_or_series).first()
        if preference:
            session.delete(preference)
            session.commit()
            print(f"Оценка для {movie_or_series} удалена.")
        else:
            print(f"Оценка для {movie_or_series} не найдена.")
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def manage_preference():
    action = input(
        "Что вы хотите сделать? \nВведите 'a' для добавления/изменения оценки \nВведите 'd' для удаления \n======>").strip().lower()
    username = input("Введите имя пользователя: ").strip()
    movie_or_series = input("Введите название фильма или сериала: ").strip()

    if action == 'a':
        rating = float(input("Введите оценку: ").strip())
        add_or_update_preference(username, movie_or_series, rating)
    elif action == 'd':
        delete_preference(username, movie_or_series)
    else:
        print("Неверный ввод. Пожалуйста, введите 'a' или 'd'.")


@app.route('/preference', methods=['POST'])
def add_or_update_user_preference():
    data = request.json
    username = data.get('username')
    movie_or_series = data.get('movie_or_series')
    rating = data.get('rating')

    if not all([username, movie_or_series, rating is not None]):
        return jsonify({"error": "Укажите username, movie_or_series и rating."}), 400

    try:
        rating = float(rating)
    except ValueError:
        return jsonify({"error": "Rating должен быть числом."}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    result = add_or_update_preference(user_id, username, movie_or_series, rating)
    status_code = 200 if "message" in result else 400
    return jsonify(result), status_code

# Эндпоинт для удаления предпочтения
@app.route('/preference', methods=['DELETE'])
def delete_user_preference():
    data = request.json
    username = data.get('username')
    movie_or_series = data.get('movie_or_series')

    if not all([username, movie_or_series]):
        return jsonify({"error": "Укажите username и movie_or_series."}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    result = delete_preference(user_id, movie_or_series)
    status_code = 200 if "message" in result else 400
    return jsonify(result), status_code

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(debug=True)


# Пример использования
manage_preference()
