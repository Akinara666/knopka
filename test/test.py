from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import pytest

# Инициализация базы данных
db = SQLAlchemy()


# Конфигурация приложения
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


# Функция для создания приложения
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    CORS(app)
    Migrate(app, db)

    # Пример маршрута
    @app.route('/health')
    def health():
        return jsonify({"status": "ok"}), 200

    return app


# Тесты для приложения
@pytest.fixture
def app():
    """Фикстура для создания тестового приложения."""
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Фикстура для создания тестового клиента."""
    return app.test_client()


def test_app_creation(app):
    """Проверка успешного создания приложения."""
    assert app is not None


def test_health_endpoint(client):
    """Тест на проверку работоспособности маршрута /health."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_home_endpoint(client):
    """Тест на запрос к несуществующему маршруту."""
    response = client.get('/')
    assert response.status_code == 404


if __name__ == "__main__":
    # Создаем приложение
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
