import json
import os

# Путь к файлу для хранения активных токенов
ACTIVE_TOKENS_FILE = "active_tokens.json"
blacklist_tokens = set()  # Токены в черном списке

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

def logout_user(token: str):
    """Выполняет выход пользователя, удаляя токен из активных и добавляя в черный список."""
    # Загружаем активные токены
    active_tokens = load_active_tokens()

    if token not in active_tokens:
        raise ValueError("Неверный токен или пользователь уже вышел")

    # Удаляем токен из активных и добавляем в черный список
    del active_tokens[token]
    blacklist_tokens.add(token)
    save_active_tokens(active_tokens)
    print("Выход выполнен успешно. Токен добавлен в черный список.")
    return {"message": "Выход выполнен успешно"}

# Чтение токена из файла
try:
    with open("session_token.txt", "r") as file:
        token = file.read().strip()

    # Выход пользователя
    logout_result = logout_user(token)
    print(logout_result["message"])

    # Удаляем файл токена после выхода
    os.remove("session_token.txt")

except FileNotFoundError:
    print("Ошибка: Токен не найден. Пользователь не вошел в систему.")

except ValueError as e:
    print(f"Ошибка: {e}")