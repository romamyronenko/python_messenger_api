from pydantic import BaseModel


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
    id: int
    chat_id: int
    text: str
    user_id: int
    content: str


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
