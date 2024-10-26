def is_email_taken(email: str) -> bool:
    """
    Проверяет, занят ли email.
    """
    # Заглушка, которая всегда возвращает False (email не занят)
    return False


def is_username_taken(username: str) -> bool:
    """
    Проверяет, занят ли username.
    """
    # Заглушка, которая всегда возвращает False (username не занят)
    return False


def hash_password(password: str) -> str:
    """
    Простейшая функция хеширования пароля.
    """
    return "hashed_" + password  # В реальной практике замените на безопасный хеш.


def register_user(email: str, password: str, username: str):
    """
    Регистрирует нового пользователя.
    """
    if is_email_taken(email):
        raise ValueError("Email уже занят")
    if is_username_taken(username):
        raise ValueError("Имя пользователя уже занято")

    hashed_password = hash_password(password)

    # Выводим данные как результат вместо записи в файл
    print(
        f"Зарегистрирован новый пользователь:\nEmail: {email}\nUsername: {username}\nPassword Hash: {hashed_password}")
    return {"message": "Пользователь успешно зарегистрирован"}


# Запрашиваем данные пользователя для регистрации
email = input("Введите email: ")
username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")

try:
    result = register_user(email, password, username)
    print(result["message"])
except ValueError as e:
    print(f"Ошибка: {e}")