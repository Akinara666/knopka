import jwt
import datetime
import hashlib

# Секретный ключ для генерации JWT токенов
SECRET_KEY = "your_secret_key"


def validate_reset_token(token: str) -> int:
    """
    Проверяет валидность токена для сброса пароля и возвращает user_id при успехе.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["user_id"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Токен истек")
    except jwt.InvalidTokenError:
        raise ValueError("Неверный токен")


def hash_password(password: str) -> str:
    """
    Заглушка для хеширования пароля.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def reset_password(token: str, new_password: str):
    """
    Изменяет пароль пользователя после сброса.
    """
    try:
        user_id = validate_reset_token(token)

        # Здесь изменение пароля пользователя в базе данных (заглушка)
        # user = db.session.query(User).get(user_id)
        # user.password = hash_password(new_password)
        # db.session.commit()

        hashed_password = hash_password(new_password)
        print(f"Пароль пользователя с ID {user_id} изменен на: {hashed_password}")

        return {"message": "Пароль успешно изменен"}

    except ValueError as e:
        return {"error": str(e)}


# Пример использования
# Генерация тестового токена для сброса пароля
def generate_reset_token(user_id: int) -> str:
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    return jwt.encode(
        {"user_id": user_id, "exp": expiration_time},
        SECRET_KEY,
        algorithm="HS256"
    )


# Пример работы
user_id = 123
test_token = generate_reset_token(user_id)
new_password = "new_secure_password"

result = reset_password(test_token, new_password)
print(result["message"])
