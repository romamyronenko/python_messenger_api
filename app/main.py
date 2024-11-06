from fastapi import FastAPI, Depends, WebSocket, HTTPException, status
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

import database.schema
from app.authorization import auth_router
from app.models import Message
from app.security import get_current_user, get_db
from database import engine

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


@app.post("/chat/{chat_id}/message", response_model=Message)
def send_message(
        chat_id: int,
        message: Message,
        user: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_message = Message(
        conversation_id=chat_id,
        message_text=message,
        user_id=user
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


@app.get("/chat/{chat_id}")
def get_messages(chat_id: int, user: str = Depends(get_current_user)):
    pass


@app.get("/contacts")
def get_contacts(user: str = Depends(get_current_user)):
    pass


@app.post("/chat")
def create_chat(user: str = Depends(get_current_user)):
    pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
