import pytest
from sqlalchemy.orm import Session
from sqlalchemy.testing import db

from app.main import client
from app.security import create_user, UserCreate, get_db
from database.schema import User, Message


def create_test_user(db: Session):
    user_data = UserCreate(
        username="testuser",
        email="testemail@example.com",
        password="testpassword",
        display_name="Test User",
    )
    db_user = create_user(db, user_data)
    db.commit()
    return db_user


@pytest.fixture()
def create_db_user():
    db: Session = next(get_db())
    db_user = create_test_user(db)

    yield db_user

    db.delete(db_user)
    db.commit()


@pytest.fixture()
def create_db_user_msg():
    db: Session = next(get_db())
    db_user = create_test_user(db)

    yield db_user


@pytest.fixture()
def login_test_user():
    response = client.post(
        "/auth/login/", json={"username": "testuser", "password": "testpassword"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function", autouse=True)
def cleanup_db():
    db: Session = next(get_db())
    try:
        yield
    finally:
        db.query(Message).delete()
        db.query(User).delete()
        db.commit()
        db.close()


