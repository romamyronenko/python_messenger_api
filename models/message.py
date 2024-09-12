from pydantic import BaseModel


class Message(BaseModel):
    id: int
    chat_id: int
    text: str
    user_id: int
