from typing import List

from fastapi import FastAPI, Depends, HTTPException, WebSocket, status
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

import database
from ai_tools.ai_translate import translate
from app.authorization import auth_router
from app.connection_manager import manager
from app.models import (
    MessageGet,
    MessageTranslateRequest,
    UserAuthResponse,
)
from app.security import get_current_user, get_db, get_current_user_from_token
from database import engine
from database.schema import Message, User

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


@app.websocket("/ws/chat/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: int,
        db: Session = Depends(get_db),
):
    """
    WebSocket endpoint for chatting
    :param websocket: WebSocket object
    :param chat_id: id of the chat
    :param user: user object
    :param db: database session
    :return: None
    """
    user = await get_current_user_from_token(websocket, db)
    if user is None:
        return

    await manager.connect(chat_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            payload = data.get("payload")

            if action == "send_message":
                message_text = payload.get("message_text")
                save_message(chat_id, message_text, user.id, db)

                await manager.broadcast(chat_id, f"User {user.username} says: {message_text}")
            elif action == "translate":
                message_text = payload.get("message_text")
                language = payload.get("language")

                message_request = MessageTranslateRequest(
                    message_text=message_text,
                    language=language
                )

                translated_message = ai_translate(
                    chat_id=chat_id,
                    message=message_request,
                    user=user,
                    db=db
                )
                await manager.broadcast(chat_id, f"Translated message: {translated_message.translated_text}")
            # TODO: Add support for other actions (messages translation, etc.)
            else:
                await websocket.send_text("Unsupported action")
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)


def save_message(
        chat_id: int,
        message_text: str,
        user_id: int,
        db: Session,
):
    """
    Saves message to the database
    :param chat_id: id of the chat
    :param message_text: text of the message
    :param user_id: id of the user who sent the message
    :param db: database session
    :return: Message object
    """
    db_message = Message(
        conversation_id=chat_id,
        message_text=message_text,
        user_id=user_id,
    )

    db.add(db_message)
    try:
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/chat/{chat_id}/message", response_model=List[MessageGet])
def get_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == chat_id).all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No messages found for chat_id: {chat_id}",
        )

    return messages


def ai_translate(
        chat_id: int,
        message: MessageTranslateRequest,
        user: User,
        db: Session,
):
    """"AI-traslation handler"""
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


def save_translated_message(db: Session, data: dict) -> Message:
    translated_message = Message(
        conversation_id=data["chat_id"],
        message_text=data["message_text"],
        translated_text=data["translated_text"],
        language=data["language"],
        user_id=data["user_id"],
    )
    db.add(translated_message)
    try:
        db.commit()
        db.refresh(translated_message)
        return translated_message
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/username", response_model=UserAuthResponse)
def get_username(current_user: User = Depends(get_current_user)):
    return UserAuthResponse(username=current_user.username)


@app.get("/contacts")
def get_contacts(user: str = Depends(get_current_user)):
    pass


@app.post("/chat")
def create_chat(user: str = Depends(get_current_user)):
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
