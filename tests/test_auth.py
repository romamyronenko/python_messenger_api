from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register(cleanup_user):
    response = client.post("/auth/register/", json={
        "username": "testuser",
        "email": "testemail@example.com",
        "password": "testpassword",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_login_success(create_db_user):
    response = client.post("/auth/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post("/auth/login/", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_protected_resource(create_db_user):
    login_response = client.post("/auth/login/", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    response = client.get("/auth/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_protected_resource_without_token():
    response = client.get("/auth/users/me")
    assert response.status_code == 401
