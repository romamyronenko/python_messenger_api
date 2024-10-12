from fastapi import FastAPI, Depends, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

import database.schema
from app.authorization import auth_router
from app.models import Message
from app.security import get_current_user
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


@app.post("/chat/{chat_id}")
def send_message(chat_id: int, message: Message, user: str = Depends(get_current_user)):
    pass


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
