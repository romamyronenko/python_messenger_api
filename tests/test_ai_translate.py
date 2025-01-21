from unittest.mock import patch, MagicMock, Mock

from fastapi.testclient import TestClient
from sqlalchemy.testing import db

from app.main import app
from app.models import MessageTranslateRequest

client = TestClient(app)


class TestTranslateEndpoint:

    @patch('app.main.translate')
    def test_ai_translate(self, mock_translate, create_db_user_msg, login_test_user):
        mock_translate.return_value = "Translated text"

        chat_id = 1
        request_payload = {
            "message_text": "Hello, this is a test message",
            "language": "fr"
        }

        response = client.post(
            f"/chat/{chat_id}/translate",
            json=request_payload,
            headers={"Authorization": f"Bearer {login_test_user}"},
        )

        assert response.status_code == 200
        assert response.json()["translated_text"] == "Translated text"

        mock_translate.assert_called_once_with(
            MessageTranslateRequest(
                message_text="Hello, this is a test message",
                language="fr",
            ),
            language="fr"
        )
