from fastapi.testclient import TestClient
from app.main import app
import random
import string

client = TestClient(app)

def generate_unique_username():
    return ''.join(random.choices(string.ascii_lowercase, k=10))

def test_register():
    unique_username = generate_unique_username()
    response = client.post("/register/", json={
        "username": unique_username,
        "email": f"{unique_username}@example.com",
        "password": "testpassword",
        "full_name": "Test User"
    })
    print(response.json())
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_login_success():
    response = client.post("/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/login/", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_protected_resource():
    login_response = client.post("/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_protected_resource_without_token():
    response = client.get("/users/me")
    assert response.status_code == 401