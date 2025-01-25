from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

import database
from ai_tools.ai_translate import translate
from app.authorization import auth_router
from app.models import (
    MessageSent,
    MessageGet,
    MessageTranslateResponse,
    MessageTranslateRequest,
)
from app.security import get_current_user, get_db
from database import engine
from database.schema import Message, Conversation

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
def get_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == chat_id).all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No messages found for chat_id: {chat_id}",
        )

    return messages


def save_translated_message(db: Session, data: dict) -> Message:
    translated_message = Message(
        conversation_id=data["chat_id"],
        message_text=data["message_text"],
        translated_text=data["translated_text"],
        language=data["language"],
        user_id=data["user_id"],
    )
    db.add(translated_message)
    db.commit()
    db.refresh(translated_message)
    return translated_message


@app.post("/chat/{chat_id}/translate", response_model=MessageTranslateResponse)
def ai_translate(
    chat_id: int,
    message: MessageTranslateRequest,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not message.message_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message text cannot be empty.",
        )

    try:

        translation = translate(message, language=message.language)

        data = {
            "chat_id": chat_id,
            "message_text": message.message_text,
            "translated_text": translation,
            "language": message.language,
            "user_id": user.id,
        }

        translated_message = save_translated_message(db=db, data=data)
        return translated_message

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/contacts")
def get_contacts(user: str = Depends(get_current_user)):
    pass


@app.post("/chat")
def create_chat(user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = Conversation()
    db.add(chat)
    db.flush([chat])
    return chat.id


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
