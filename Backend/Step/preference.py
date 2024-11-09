from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

DATABASE_URL_PREFS = "sqlite:///user_preferences.db"
engine_prefs = create_engine(DATABASE_URL_PREFS)
BasePrefs = declarative_base()
SessionPrefs = sessionmaker(bind=engine_prefs)


class UserPreference(BasePrefs):
    __tablename__ = 'user_preferences'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    movie_or_series = Column(String, nullable=False)  # Обратите внимание, что это поле должно присутствовать
    rating = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


# Пересоздаем таблицу, если база данных очищена
BasePrefs.metadata.create_all(engine_prefs)
