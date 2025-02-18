import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

import database
from app.authorization import auth_router
from app.models import MessageSent, MessageGet
from app.security import get_current_user, get_db
from database import engine
from database.schema import Message, Conversation, ConversationParticipant, User

database.schema.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
client = TestClient(app)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"hello": "world"}


@app.post("/chat/{chat_id}/message", response_model=MessageSent)
def send_message(
        chat_id: int,
        message: MessageSent,
        user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    db_message = Message(
        conversation_id=chat_id, message_text=message.message_text, user_id=user.id
    )
    db.add(db_message)

    try:
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/chat/{chat_id}/message", response_model=List[MessageGet])
def get_messages_from_chat(
        chat_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(Message.conversation_id == chat_id).all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No messages found for chat_id: {chat_id}",
        )

    return messages


@app.get("/chats")
def get_user_chats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chats = db.query(ConversationParticipant).filter(ConversationParticipant.user_id == user.id).all()
    print(db.query(ConversationParticipant).all())
    print(user.id)
    return chats


@app.get("/contacts")
def get_contacts(user: str = Depends(get_current_user)):
    pass


class UserIds(BaseModel):
    users_ids: list[int]


@app.post("/chat")
def create_chat(users_ids: UserIds, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = Conversation()
    db.add(chat)
    db.flush([chat])
    conv_user = ConversationParticipant(user_id=user.id, conversation_id=chat.id, joined_at=datetime.datetime.now())
    db.add(conv_user)
    if users_ids.users_ids:
        for user_id in users_ids.users_ids:
            db.add(ConversationParticipant(user_id=user_id, conversation_id=chat.id, joined_at=datetime.datetime.now()))
    db.commit()
    return chat.id


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app")
