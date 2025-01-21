from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.models import MessageTranslateResponse

client = TestClient(app)


class TestTranslateEndpoint:

    @patch("app.main.translate")
    @patch("app.main.save_translated_message")
    def test_ai_translate(self, mock_translate, mock_save_translated_message,
                          create_db_user_msg, login_test_user):
        mock_translate.return_value = MessageTranslateResponse(
            conversation_id=1,
            message_text="Hello, this is a test message",
            translated_text="Translated text",
            language="fr",
            user_id=1
        )

        mock_save_translated_message.return_value = MessageTranslateResponse(
            conversation_id=1,
            message_text="Hello, this is a test message",
            translated_text="Translated text",
            language="fr",
            user_id=1
        )

        chat_id = 1
        request_payload = {
            "message_text": "Hello, this is a test message",
            "language": "fr",
        }

        response = client.post(
            f"/chat/{chat_id}/translate",
            json=request_payload,
            headers={"Authorization": f"Bearer {login_test_user}"},
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["conversation_id"] == 1
        assert response_data["message_text"] == "Hello, this is a test message"
        assert response_data["translated_text"] == "Translated text"
        assert response_data["language"] == "fr"
        assert response_data["user_id"] == 1

        mock_translate.assert_called_once()

        mock_save_translated_message.assert_called_once()
