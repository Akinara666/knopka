from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt
import secrets
import datetime
from flask_cors import CORS

# Настройка приложения Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Настройка баз данных SQLite
DATABASE_URL = "sqlite:///mydatabase.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Модели базы данных
class UserLogin(Base):
    __tablename__ = 'user_logins'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AuthorizedUser(Base):
    __tablename__ = 'authorized_users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    login_token = Column(String, nullable=False)
    login_time = Column(DateTime, default=datetime.datetime.utcnow)

class UserWatchLater(Base):
    __tablename__ = 'user_wl'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserLike(Base):
    __tablename__ = 'user_like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)
    like = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        CheckConstraint('like IN (0, 1)', name='check_like_in_0_1'),
    )

class UserPreference(Base):
    __tablename__ = 'user_preferences'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Создание таблиц
Base.metadata.create_all(engine)

# Функции регистрации, логина, выхода
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "Отсутствуют данные запроса."}), 400

    username, email, password, confirm_password = data.get('username'), data.get('email'), data.get('password'), data.get('confirm_password')

    if not all([username, email, password, confirm_password]):
        return jsonify({"error": "Укажите username, email, password и confirm_password."}), 400

    if password != confirm_password:
        return jsonify({"error": "Пароли не совпадают"}), 400

    if session.query(UserLogin).filter((UserLogin.email == email) | (UserLogin.username == username)).first():
        return jsonify({"error": "Email или имя пользователя уже заняты"}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = UserLogin(username=username, password_hash=hashed_password, email=email)
    session.add(new_user)
    session.commit()
    return jsonify({"message": "Пользователь успешно зарегистрирован."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "Отсутствуют данные запроса."}), 400

    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify({"error": "Укажите username и password."}), 400

    print(f"Login attempt for user: {username}")
    user = session.query(UserLogin).filter_by(username=username).first()

    if not user:
        print("User not found")
        return jsonify({"error": "Неправильный логин или пароль"}), 400

    if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        print("Password mismatch")
        return jsonify({"error": "Неправильный логин или пароль"}), 400

    token = secrets.token_hex(16)
    authorized_user = session.query(AuthorizedUser).filter_by(user_id=user.user_id).first()

    if authorized_user:
        authorized_user.login_token = token
        authorized_user.login_time = datetime.datetime.utcnow()
    else:
        session.add(AuthorizedUser(user_id=user.user_id, username=user.username, login_token=token))

    session.commit()
    print(f"Login successful, token generated: {token}")
    return jsonify({"token": token}), 200

@app.route('/logout', methods=['POST'])
def logout():
    token = request.json.get('token')
    if not token:
        return jsonify({"error": "Отсутствует токен."}), 400

    authorized_user = session.query(AuthorizedUser).filter_by(login_token=token).first()

    if not authorized_user:
        return jsonify({"error": "Токен не найден"}), 400

    session.delete(authorized_user)
    session.commit()
    return jsonify({"message": "Выход выполнен успешно."}), 200

# Функции для "Смотреть позже" и лайков
@app.route('/watch-later', methods=['POST'])
def add_watch_later():
    data = request.json
    username, movie_or_series = data.get('username'), data.get('movie_or_series')
    user = session.query(UserLogin).filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    watch_later = UserWatchLater(user_id=user.user_id, username=username, movie_or_series=movie_or_series)
    session.add(watch_later)
    session.commit()
    return jsonify({"message": "Добавлено в список 'Смотреть позже'"}), 200

@app.route('/like', methods=['POST'])
def add_like():
    data = request.json
    username, movie_or_series, like_value = data.get('username'), data.get('movie_or_series'), data.get('like')
    user = session.query(UserLogin).filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    like = UserLike(user_id=user.user_id, username=username, movie_or_series=movie_or_series, like=like_value)
    session.add(like)
    session.commit()
    return jsonify({"message": "Оценка добавлена"}), 200

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

    user = session.query(UserLogin).filter_by(username=username).first()
    if not user:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    preference = session.query(UserPreference).filter_by(user_id=user.user_id, movie_or_series=movie_or_series).first()
    if preference:
        preference.rating = rating
        preference.updated_at = datetime.datetime.utcnow()
    else:
        new_preference = UserPreference(user_id=user.user_id, username=username, movie_or_series=movie_or_series, rating=rating)
        session.add(new_preference)

    session.commit()
    return jsonify({"message": "Оценка успешно добавлена/обновлена."}), 200

@app.route('/preference', methods=['DELETE'])
def delete_user_preference():
    data = request.json
    username = data.get('username')
    movie_or_series = data.get('movie_or_series')

    if not all([username, movie_or_series]):
        return jsonify({"error": "Укажите username и movie_or_series."}), 400

    user = session.query(UserLogin).filter_by(username=username).first()
    if not user:
        return jsonify({"error": f"Пользователь {username} не найден."}), 404

    preference = session.query(UserPreference).filter_by(user_id=user.user_id, movie_or_series=movie_or_series).first()
    if preference:
        session.delete(preference)
        session.commit()
        return jsonify({"message": "Оценка успешно удалена."}), 200
    else:
        return jsonify({"error": "Оценка не найдена."}), 404

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
