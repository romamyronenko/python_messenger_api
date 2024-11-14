import pytest
from sqlalchemy.orm import Session

from app.main import client
from app.security import create_user, UserCreate, get_db, get_user
from database.schema import User, Message


@pytest.fixture()
def create_db_user():
    db: Session = next(get_db())
    user_data = UserCreate(
        username="testuser",
        email="testemail@example.com",
        password="testpassword",
        display_name="Test User",
    )
    db_user = create_user(db, user_data)
    db.commit()

    yield db_user

    db.delete(db_user)
    db.commit()


@pytest.fixture()
def create_db_user_msg():
    db: Session = next(get_db())
    user_data = UserCreate(
        username="testuser",
        email="testemail@example.com",
        password="testpassword",
        display_name="Test User",
    )
    db_user = create_user(db, user_data)
    db.commit()

    yield db_user


@pytest.fixture()
def cleanup_user():
    yield

    db = next(get_db())
    user = get_user(db, username="testuser")
    if user:
        db.delete(user)
        db.commit()


@pytest.fixture()
def login_test_user(create_db_user_msg):
    response = client.post(
        "/auth/login/", json={"username": "testuser", "password": "testpassword"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function", autouse=True)
def cleanup_db():
    db: Session = next(get_db())
    db.query(Message).delete()
    db.query(User).delete()
    db.commit()
