from fastapi.testclient import TestClient

from app.main import app
from app.security import get_db
from database.schema import Message

client = TestClient(app)


def test_send_message(cleanup_db, create_db_user_msg, login_test_user):
    chat_id = 1

    message_data = {
        "conversation_id": chat_id,
        "message_text": "Hello, this is a test message",
        "user_id": create_db_user_msg.id,
    }

    response = client.post(
        f"/chat/{chat_id}/message",
        json=message_data,
        headers={"Authorization": f"Bearer {login_test_user}"},
    )

    print("Response status:", response.status_code)
    print("Response content:", response.json())

    assert response.status_code == 200
    response_data = response.json()

    assert response_data["conversation_id"] == chat_id
    assert response_data["message_text"] == "Hello, this is a test message"
    assert response_data["user_id"] == create_db_user_msg.id

    db = next(get_db())
    message_in_db = db.query(Message).filter(Message.id).first()
    assert message_in_db is not None, "Message not found in database"
    assert message_in_db.message_text == "Hello, this is a test message"


def test_get_message(cleanup_db, create_db_user_msg, login_test_user):
    chat_id = 1
    db = next(get_db())

    message = Message(
        conversation_id=chat_id,
        message_text="Hello, this is a test message",
        user_id=create_db_user_msg.id,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    response = client.get(
        f"/chat/{chat_id}/message",
        headers={"Authorization": f"Bearer {login_test_user}"},
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    response_data = response.json()
    assert isinstance(response_data, list), "Response data should be a list"
    assert len(response_data) == 1, f"Expected 1 message, got {len(response_data)}"

    retrieved_message = response_data[0]
    assert retrieved_message["conversation_id"] == chat_id, "Incorrect conversation_id"
    assert (
            retrieved_message["message_text"] == "Hello, this is a test message"
    ), "Incorrect message_text"
