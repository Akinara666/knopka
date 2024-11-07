from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import inspect
from bcrypt import hashpw, gensalt

# Настройка базы данных SQLite
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Базовый класс для определения таблиц
Base = declarative_base()


# Определение таблицы для логинов пользователей
class UserLogin(Base):
    __tablename__ = 'user_logins'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())


# Создание таблицы в базе данных
Base.metadata.create_all(engine)

# Проверка создания таблицы
inspector = inspect(engine)
print("Таблицы в базе данных:", inspector.get_table_names())
print("Таблица user_logins успешно создана.")

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()


# Функция для добавления нового пользователя
def add_user(username, plain_text_password, email):
    # Хеширование пароля
    password_hash = hashpw(plain_text_password.encode(), gensalt())

    # Создание нового пользователя
    new_user = UserLogin(username=username, password_hash=password_hash, email=email)

    # Добавление и сохранение в базе данных
    session.add(new_user)
    session.commit()
    print(f"User {username} added successfully.")


# Пример добавления пользователя
add_user('testuser', 'securepassword', 'testuser@example.com')
