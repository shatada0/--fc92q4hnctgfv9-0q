"""ЛР5: те же проверки, что в коллекции postman/lab5.postman_collection.json, на requests + pytest."""
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
NEW_USER = {"name": "Иван Петров", "username": "ivan", "email": "ivan@example.com"}
UPDATED_USER = {"id": 1, "name": "Иван Петров", "email": "ivan.new@example.com"}
USER_SCHEMA = {"id": int, "name": str, "username": str, "email": str, "address": dict, "company": dict}


def test_get_user():
    response = requests.get(f"{BASE_URL}/users/1", timeout=10)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert response.elapsed.total_seconds() < 2
    user = response.json()
    for key, value_type in USER_SCHEMA.items():
        assert isinstance(user[key], value_type), key
    assert user["id"] == 1
    assert user["name"] == "Leanne Graham"
    assert user["email"] == "Sincere@april.biz"


def test_create_user():
    response = requests.post(f"{BASE_URL}/users", json=NEW_USER, timeout=10)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert {key: body[key] for key in NEW_USER} == NEW_USER


def test_update_user():
    response = requests.put(f"{BASE_URL}/users/1", json=UPDATED_USER, timeout=10)

    assert response.status_code == 200
    assert response.json() == UPDATED_USER


def test_get_missing_user():
    response = requests.get(f"{BASE_URL}/users/9999", timeout=10)

    assert response.status_code == 404
    assert response.json() == {}
