import uuid
import json

# Путь к файлу для хранения активных токенов
ACTIVE_TOKENS_FILE = "active_tokens.json"


def load_active_tokens():
    """Загружает активные токены из файла."""
    try:
        with open(ACTIVE_TOKENS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_active_tokens(tokens):
    """Сохраняет активные токены в файл."""
    with open(ACTIVE_TOKENS_FILE, "w") as file:
        json.dump(tokens, file)


def generate_token() -> str:
    """Генерирует уникальный токен для сессии."""
    return str(uuid.uuid4())


def is_valid_email(email: str) -> bool:
    """Проверяет, существует ли пользователь с данным email."""
    return True  # Заглушка: email всегда считается существующим


def is_correct_password(email: str, password: str) -> bool:
    """Проверяет, соответствует ли пароль указанному email."""
    return hash_password(password) == "hashed_" + password  # Заглушка для проверки пароля


def hash_password(password: str) -> str:
    """Простейшая функция хеширования пароля."""
    return "hashed_" + password


def login_user(email: str, password: str):
    """Выполняет вход пользователя и создает токен сессии."""
    if not is_valid_email(email) or not is_correct_password(email, password):
        raise ValueError("Неверный email или пароль")

    # Загружаем активные токены
    active_tokens = load_active_tokens()

    # Генерируем токен и сохраняем его как активный
    token = generate_token()
    active_tokens[token] = email
    save_active_tokens(active_tokens)
    print(f"Вход выполнен успешно. Токен сессии: {token}")

    # Сохраняем токен в файл для дальнейшего использования при выходе
    with open("session_token.txt", "w") as file:
        file.write(token)

    return {"message": "Вход выполнен успешно", "token": token}


# Пример работы
email = input("Введите email: ")
password = input("Введите пароль: ")

try:
    # Вход пользователя
    login_result = login_user(email, password)
    print(login_result["message"])

except ValueError as e:
    print(f"Ошибка: {e}")