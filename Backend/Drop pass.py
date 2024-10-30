import jwt
import datetime

# Секретный ключ для генерации JWT токенов
SECRET_KEY = "your_secret_key"

def generate_reset_token(user_id: int) -> str:
    """
    Генерирует одноразовый токен сброса пароля с использованием JWT.
    """
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
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

def send_password_reset_email(email: str):
    """
    Отправляет письмо для сброса пароля.
    """
    # Здесь проверка на существование пользователя в базе данных (заглушка)
    user_id = 123  # Предполагаем, что такой пользователь существует
    if user_id:
        reset_token = generate_reset_token(user_id)
        reset_link = f"http://yourapp.com/reset-password/{reset_token}"
        send_email(email, f"Ссылка для сброса пароля: {reset_link}")
        return {"message": "Инструкции по сбросу пароля отправлены на email"}
    else:
        raise ValueError("Пользователь с таким email не найден")

# Пример использования
email = "user@example.com"
try:
    result = send_password_reset_email(email)
    print(result["message"])
except ValueError as e:
    print(f"Ошибка: {e}")
