import pytest

from app.security import create_user, UserCreate, get_db


@pytest.fixture()
def create_db_user():
    db = next(get_db())
    user = UserCreate(username='testuser', email='testemail@example.com', password='testpassword',
                      full_name='Test User')
    db_user = create_user(db, user)

    yield db_user

    db.delete(db_user)
    db.commit()
