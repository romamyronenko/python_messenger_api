from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class UserCreatedResponse(BaseModel):
    message: str
    id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserAuthRequest(BaseModel):
    username: str
    password: str


class Message(BaseModel):
    conversation_id: int
    message_text: str
    user_id: int
    content: Optional[str] = None
    sent_at: Optional[datetime] = None


class MessageSent(BaseModel):
    conversation_id: Optional[int]
    message_text: str
    user_id: Optional[int]


class MessageGet(BaseModel):
    conversation_id: int
    message_text: str

    class Config:
        orm_mode = True


class MessageTranslateRequest(BaseModel):
    message_text: str
    language: Optional[str]


class MessageTranslateResponse(BaseModel):
    conversation_id: int
    user_id: int
    message_text: str
    translated_text: str
    language: str


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
