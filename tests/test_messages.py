from fastapi.testclient import TestClient

from app.main import app
from database.schema import Message
from app.security import get_db

client = TestClient(app)


def test_send_message(cleanup_db, create_db_user_msg, login_test_user):
    chat_id = 1  # Example chat ID, make sure it exists in your test DB

    # Define the message to be sent
    message_data = {
        "conversation_id": chat_id,
        "message_text": "Hello, this is a test message",
        "user_id": create_db_user_msg.id
    }

    # Make the request to send the message with authentication
    response = client.post(
        f"/chat/{chat_id}/message",
        json=message_data,
        headers={"Authorization": f"Bearer {login_test_user}"}
    )

    print("Response status:", response.status_code)
    print("Response content:", response.json())
    # Assert response is successful
    assert response.status_code == 200
    response_data = response.json()

    # Validate response data structure
    assert response_data["conversation_id"] == chat_id
    assert response_data["message_text"] == "Hello, this is a test message"
    assert response_data["user_id"] == create_db_user_msg.id

    # # Check that the message was indeed created in the database
    db = next(get_db())
    message_in_db = db.query(Message).filter(Message.id).first()
    assert message_in_db is not None, "Message not found in database"
    assert message_in_db.message_text == "Hello, this is a test message"
