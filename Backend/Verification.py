import jwt
import datetime

# Секретный ключ для генерации JWT токенов
SECRET_KEY = "your_secret_key"

def generate_confirmation_token(user_id: int) -> str:
    """
    Генерирует одноразовый токен подтверждения с использованием JWT.
    """
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    token = jwt.encode(
        {"user_id": user_id, "exp": expiration_time},
        SECRET_KEY,
        algorithm="HS256"
    )
    return token

def send_email(email: str, content: str):
    """
    Заглушка для отправки письма.
    """
    print(f"Отправка письма на {email}: {content}")

def send_confirmation_email(user_id: int, email: str):
    """
    Отправляет подтверждение на email пользователя.
    """
    confirmation_token = generate_confirmation_token(user_id)
    confirmation_link = f"http://yourapp.com/confirm/{confirmation_token}"
    send_email(email, f"Ссылка для подтверждения: {confirmation_link}")
    return {"message": "Подтверждение отправлено на email"}

# Пример использования
user_id = 123
email = "user@example.com"

result = send_confirmation_email(user_id, email)
print(result["message"])
