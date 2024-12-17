import pytest
import requests

# Если у вас FastAPI
from app.main import app


# Получаем список всех эндпоинтов (для FastAPI)
def get_endpoints(app):
    endpoints = []
    for route in app.routes:
        methods = route.methods - {"HEAD", "OPTIONS"}  # Исключаем ненужные методы
        for method in methods:
            path = route.path.replace("{", "").replace("}", "")  # Убираем параметры
            endpoints.append({"method": method, "path": path})
    return endpoints


BASE_URL = "http://127.0.0.1:8000"  # Адрес вашего сервера


# Тесты для всех эндпоинтов
@pytest.mark.parametrize("endpoint", get_endpoints(app))
def test_endpoints(endpoint):
    url = f"{BASE_URL}{endpoint['path']}"
    method = endpoint['method']

    response = None
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json={})  # Пустой JSON
    elif method == "PUT":
        response = requests.put(url, json={})
    elif method == "DELETE":
        response = requests.delete(url)

    assert response is not None, f"Request failed for {method} {url}"
    assert response.status_code < 500, f"Server error on {method} {url}"
