def is_valid_email(email: str) -> bool:
    """
    Проверяет, существует ли пользователь с данным email.
    """
    # Заглушка, которая всегда возвращает True (email существует)
    return True


def is_correct_password(email: str, password: str) -> bool:
    """
    Проверяет, соответствует ли пароль указанному email.
    """
    # Заглушка, которая всегда возвращает True (пароль правильный)
    hashed_password = hash_password(password)
    return hashed_password == "hashed_" + password


def hash_password(password: str) -> str:
    """
    Простейшая функция хеширования пароля.
    """
    return "hashed_" + password  # В реальной практике замените на безопасный хеш.


def login_user(email: str, password: str):
    """
    Выполняет вход пользователя.
    """
    if not is_valid_email(email):
        raise ValueError("Неверный email или пароль")

    if not is_correct_password(email, password):
        raise ValueError("Неверный email или пароль")

    return {"message": "Вход выполнен успешно"}


# Запрашиваем данные пользователя для входа
email = input("Введите email: ")
password = input("Введите пароль: ")

try:
    result = login_user(email, password)
    print(result["message"])
except ValueError as e:
    print(f"Ошибка: {e}")