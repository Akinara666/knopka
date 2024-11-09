import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL_PREFS = "sqlite:///user_preferences.db"
engine_prefs = create_engine(DATABASE_URL_PREFS)
BasePrefs = declarative_base()
SessionPrefs = sessionmaker(bind=engine_prefs)

class UserPreference(BasePrefs):
    __tablename__ = 'user_preferences'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc),
                        onupdate=datetime.datetime.now(datetime.timezone.utc))

# Пересоздаем таблицу, если база данных очищена
BasePrefs.metadata.create_all(engine_prefs)

def add_or_update_preference(username, movie_or_series, rating):
    session = SessionPrefs()
    try:
        preference = session.query(UserPreference).filter_by(username=username, movie_or_series=movie_or_series).first()
        if preference:
            preference.rating = rating
            preference.updated_at = datetime.datetime.now(datetime.timezone.utc)
            print(f"Оценка для {movie_or_series} обновлена на {rating}.")
        else:
            new_preference = UserPreference(
                username=username,
                movie_or_series=movie_or_series,
                rating=rating,
                updated_at=datetime.datetime.now(datetime.timezone.utc)
            )
            session.add(new_preference)
            print(f"Оценка для {movie_or_series} добавлена.")
        session.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def delete_preference(username, movie_or_series):
    session = SessionPrefs()
    try:
        preference = session.query(UserPreference).filter_by(username=username, movie_or_series=movie_or_series).first()
        if preference:
            session.delete(preference)
            session.commit()
            print(f"Оценка для {movie_or_series} удалена.")
        else:
            print(f"Оценка для {movie_or_series} не найдена.")
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

def manage_preference():
    action = input(
        "Что вы хотите сделать? \nВведите 'a' для добавления/изменения оценки \nВведите 'd' для удаления \n======>").strip().lower()
    username = input("Введите имя пользователя: ").strip()
    movie_or_series = input("Введите название фильма или сериала: ").strip()

    if action == 'a':
        rating = float(input("Введите оценку: ").strip())
        add_or_update_preference(username, movie_or_series, rating)
    elif action == 'd':
        delete_preference(username, movie_or_series)
    else:
        print("Неверный ввод. Пожалуйста, введите 'a' или 'd'.")

# Пример использования
manage_preference()
