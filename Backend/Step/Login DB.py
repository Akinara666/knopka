from sqlalchemy import Column, Integer, String, DateTime, create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import bcrypt

# Подключение к базе данных
engine = create_engine('sqlite:///users.db')
Base = declarative_base()

# Настройка сессии
Session = sessionmaker(bind=engine)
session = Session()


class UserLogin(Base):
    __tablename__ = 'user_logins'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # Добавляем ограничение уникальности
    __table_args__ = (UniqueConstraint('username', 'email', name='uix_1'),)

# Создание таблицы в базе данных
Base.metadata.create_all(engine)
print("Таблица user_logins успешно создана.")


def add_user(username, password, email):
    # Хешируем пароль с использованием bcrypt
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Проверка на существование пользователя с таким же email или username
    existing_user = session.query(UserLogin).filter(
        (UserLogin.email == email) | (UserLogin.username == username)
    ).first()

    if existing_user:
        print("Пользователь с таким email или username уже существует.")
        return None

    # Создаем нового пользователя
    new_user = UserLogin(
        username=username,
        password_hash=password_hash.decode('utf-8'),
        email=email,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # Добавляем пользователя в сессию и сохраняем изменения
    try:
        session.add(new_user)
        session.commit()
        print(f"Пользователь {username} успешно добавлен.")
    except IntegrityError:
        session.rollback()
        print("Ошибка при добавлении пользователя. Возможно, email или username уже существуют.")

# Добавляем тестового пользователя
add_user('fred', 'fred', 'fred@example.com')
