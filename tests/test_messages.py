import json

import pytest
import websockets
from fastapi.testclient import TestClient

from app.main import app
from app.security import get_db
from database.schema import Message

client = TestClient(app)

CHAT_ID = 1
WS_URL = f"ws://localhost:8000/ws/chat/{CHAT_ID}"


# change to @pytest.mark.asyncio after migration to PostgreSQL
@pytest.mark.skip(reason="Waiting for PostgreSQL DB")
async def test_websocket_send_message(create_db_user_msg, login_test_user):
    token = login_test_user

    headers = {"Authorization": f"Bearer {token}"}

    async with websockets.connect(WS_URL, additional_headers=headers) as websocket:
        await websocket.send(json.dumps({
            "action": "send_message",
            "payload": {
                "message_text": "Test message"
            }
        }))

        response = await websocket.recv()
        data = json.loads(response)

        assert data["action"] == "send_message"
        assert data["payload"]["message_text"] == "Test message"


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
