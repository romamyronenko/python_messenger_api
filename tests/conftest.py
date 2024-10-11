import pytest

from app.security import create_user, UserCreate, get_db, get_user


@pytest.fixture()
def create_db_user():
    db = next(get_db())
    user = UserCreate(
        username="testuser",
        email="testemail@example.com",
        password="testpassword",
        display_name="Test User",
    )
    db_user = create_user(db, user)

    yield db_user

    db.delete(db_user)
    db.commit()


@pytest.fixture()
def cleanup_user():
    yield

    db = next(get_db())
    user = get_user(db, username="testuser")
    if user:
        db.delete(user)
        db.commit()
