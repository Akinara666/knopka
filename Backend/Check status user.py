import jwt
import datetime

# Секретный ключ для генерации JWT токенов
SECRET_KEY = "your_secret_key"

def validate_jwt_token(token: str) -> int:
    """
    Проверяет, действителен ли JWT токен пользователя и возвращает user_id при успехе.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["user_id"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Токен истек")
    except jwt.InvalidTokenError:
        raise ValueError("Неверный токен")

def is_email_confirmed(token: str) -> bool:
    """
    Проверяет, подтвердил ли пользователь свой email, исходя из данных токена.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token.get("is_confirmed", False)
    except jwt.InvalidTokenError:
        raise ValueError("Неверный токен")

# Пример работы с токеном, содержащим статус подтверждения email
def generate_user_token(user_id: int, is_confirmed: bool) -> str:
    """
    Генерирует JWT токен, содержащий информацию о подтверждении email.
    """
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    return jwt.encode(
        {"user_id": user_id, "is_confirmed": is_confirmed, "exp": expiration_time},
        SECRET_KEY,
        algorithm="HS256"
    )

# Тестирование
user_id = 123
is_confirmed = True  # Или False, если email не подтвержден
test_token = generate_user_token(user_id, is_confirmed)

# Проверка токена и подтверждения email
try:
    if validate_jwt_token(test_token):
        if is_email_confirmed(test_token):
            print("Пользователь авторизован и email подтвержден")
        else:
            print("Email пользователя не подтвержден")
except ValueError as e:
    print(f"Ошибка: {e}")
