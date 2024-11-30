import datetime
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, CheckConstraint
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

class UserLike(BasePrefs):
    __tablename__ = 'user_like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # Добавленный столбец
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)
    like = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc),
                        onupdate=datetime.datetime.now(datetime.timezone.utc))

    __table_args__ = (
        CheckConstraint('like IN (0, 1)', name='check_like_in_0_1'),  # Ограничение для рейтинга
    )


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

def add_or_update_like(username, movie_or_series, like_value):
    user_id = get_user_id(username)  # Получаем user_id пользователя
    if not user_id:
        print(f"Ошибка: Пользователь с именем {username} не найден в базе данных пользователей.")
        return

    session = SessionPrefs()
    try:
        like_record = session.query(UserLike).filter_by(user_id=user_id, movie_or_series=movie_or_series).first()
        if like_record:
            like_record.like = like_value  # Обновляем оценку
            like_record.updated_at = datetime.datetime.now(datetime.timezone.utc)
            print(f"Оценка для {movie_or_series} обновлена на {like_value}.")
        else:
            new_like = UserLike(
                user_id=user_id,
                username=username,
                movie_or_series=movie_or_series,
                like=like_value,
                updated_at=datetime.datetime.now(datetime.timezone.utc)
            )
            session.add(new_like)
            print(f"Оценка для {movie_or_series} добавлена.")
        session.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def delete_like(username, movie_or_series):
    user_id = get_user_id(username)
    if not user_id:
        print(f"Ошибка: Пользователь с именем {username} не найден в базе данных пользователей.")
        return

    session = SessionPrefs()
    try:
        like_record = session.query(UserLike).filter_by(user_id=user_id, movie_or_series=movie_or_series).first()
        if like_record:
            session.delete(like_record)
            session.commit()
            print(f"Оценка для {movie_or_series} удалена.")
        else:
            print(f"Оценка для {movie_or_series} не найдена.")
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def manage_like():
    action = input(
        "Что вы хотите сделать? \nВведите 'a' для добавления/изменения оценки \nВведите 'd' для удаления \n======>").strip().lower()
    username = input("Введите имя пользователя: ").strip()
    movie_or_series = input("Введите название фильма или сериала: ").strip()

    if action == 'a':
        try:
            like_value = float(input("Введите оценку (0 или 1): ").strip())
            if like_value not in [0, 1]:
                print("Ошибка: Оценка должна быть 0 или 1.")
                return
            add_or_update_like(username, movie_or_series, like_value)
        except ValueError:
            print("Ошибка: Введите число для оценки.")
    elif action == 'd':
        delete_like(username, movie_or_series)
    else:
        print("Неверный ввод. Пожалуйста, введите 'a' или 'd'.")


# Эндпоинт для добавления или обновления лайка
@app.route('/like', methods=['POST'])
def like():
    data = request.json
    username = data.get('username')
    movie_or_series = data.get('movie_or_series')
    like_value = data.get('like')

    if not all([username, movie_or_series, like_value in [0, 1]]):
        return jsonify({"error": "Неправильные данные. Убедитесь, что указаны username, movie_or_series, и like (0 или 1)."}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    result = add_or_update_like(user_id, username, movie_or_series, like_value)
    status_code = 200 if "message" in result else 400
    return jsonify(result), status_code


# Эндпоинт для удаления лайка
@app.route('/like', methods=['DELETE'])
def unlike():
    data = request.json
    username = data.get('username')
    movie_or_series = data.get('movie_or_series')

    if not all([username, movie_or_series]):
        return jsonify({"error": "Неправильные данные. Убедитесь, что указаны username и movie_or_series."}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    result = delete_like(user_id, movie_or_series)
    status_code = 200 if "message" in result else 400
    return jsonify(result), status_code


# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True)


# Пример использования
manage_like()
