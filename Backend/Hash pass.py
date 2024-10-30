import bcrypt

def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def check_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль, сравнивая его с хешем.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Пример использования
plain_password = "your_secure_password"
hashed = hash_password(plain_password)
print("Хешированный пароль:", hashed)

# Проверка пароля
is_correct = check_password("your_secure_password", hashed)
print("Пароль верный:", is_correct)
