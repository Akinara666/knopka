from flask import Flask, render_template, request, jsonify
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import secrets
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Настройки баз данных
DATABASE_URL_MAIN = "sqlite:///mydatabase.db"  # Основная база данных
DATABASE_URL_AUTH = "sqlite:///mydatabase.db"  # База данных авторизованных пользователей

# Настройка основной базы данных и модели
engine_main = create_engine(DATABASE_URL_MAIN)
BaseMain = declarative_base()
SessionMain = sessionmaker(bind=engine_main)


class UserLogin(BaseMain):
    __tablename__ = 'user_logins'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # храним хэш в виде строки
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc),
                        onupdate=datetime.datetime.now(datetime.timezone.utc))


# Настройка базы данных авторизованных пользователей и модели
engine_auth = create_engine(DATABASE_URL_AUTH)
BaseAuth = declarative_base()
SessionAuth = sessionmaker(bind=engine_auth)


class AuthorizedUser(BaseAuth):
    __tablename__ = 'authorized_users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    login_token = Column(String, nullable=False)
    login_time = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))


# Создаем таблицы, если их нет
BaseMain.metadata.create_all(engine_main)
BaseAuth.metadata.create_all(engine_auth)


# Функция проверки логина
def login_user(username, password):
    session_main = SessionMain()
    user = session_main.query(UserLogin).filter_by(username=username).first()
    if user:
        # Конвертируем строку хэша пароля в байты, если это строка
        password_hash = user.password_hash.encode() if isinstance(user.password_hash, str) else user.password_hash

        # Проверяем пароль, сравнивая байтовый хэш
        if bcrypt.checkpw(password.encode(), password_hash):
            # Если логин прошел, создаем токен
            token = secrets.token_hex(16)
            session_auth = SessionAuth()

            # Проверяем, существует ли уже запись об авторизованном пользователе
            authorized_user = session_auth.query(AuthorizedUser).filter_by(user_id=user.user_id).first()

            if authorized_user:
                # Обновляем токен и время логина для существующего пользователя
                authorized_user.login_token = token
                authorized_user.login_time = datetime.datetime.now(datetime.timezone.utc)
            else:
                # Добавляем новую запись об авторизованном пользователе
                new_auth_user = AuthorizedUser(
                    user_id=user.user_id,
                    username=user.username,
                    login_token=token,
                    login_time=datetime.datetime.now(datetime.timezone.utc)
                )
                session_auth.add(new_auth_user)

            session_auth.commit()
            print(f"Логин прошел успешно. Ваш временный токен: {token}")
            session_auth.close()
            return token
        else:
            print("Ошибка: неправильный логин или пароль.")
    else:
        print("Ошибка: пользователь не найден.")

    session_main.close()
    return None

# Эндпоинт для страницы логина (HTML форма)
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')  # Ваш HTML файл для логина


# Эндпоинт для логина пользователя (POST запрос)
@app.route('/login', methods=['POST'])
def login_request():
    username = request.json.get('loginUsername')
    password = request.json.get('loginPassword')

    result = login_user(username, password)
    if not result:
        return jsonify(result), 400
    else:
        return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)