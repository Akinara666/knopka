import jwt
import datetime

# Секретный ключ для генерации JWT токенов
SECRET_KEY = "your_secret_key"


def validate_confirmation_token(token: str) -> int:
    """
    Проверяет валидность токена подтверждения и возвращает user_id при успехе.
    """
    try:
        # Декодируем токен и проверяем его срок действия
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["user_id"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Токен истек")
    except jwt.InvalidTokenError:
        raise ValueError("Неверный токен")


def confirm_user(token: str):
    """
    Подтверждает аккаунт пользователя.
    """
    try:
        user_id = validate_confirmation_token(token)

        # Здесь происходит подтверждение пользователя в базе данных (заглушка)
        # user = db.session.query(User).get(user_id)
        # user.is_confirmed = True
        # db.session.commit()

        return {"message": "Аккаунт подтвержден"}

    except ValueError as e:
        return {"error": str(e)}


# Пример использования
# Генерация тестового токена
def generate_confirmation_token(user_id: int) -> str:
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    return jwt.encode(
        {"user_id": user_id, "exp": expiration_time},
        SECRET_KEY,
        algorithm="HS256"
    )


# Сгенерируем токен и попробуем его подтвердить
user_id = 123
test_token = generate_confirmation_token(user_id)
print(confirm_user(test_token))  # Ожидаемый результат: {"message": "Аккаунт подтвержден"}
