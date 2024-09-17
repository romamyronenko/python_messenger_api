from fastapi import FastAPI
from starlette.testclient import TestClient
from app.authorization import auth_router
from models import models
from models.database import engine
from models.message import Message

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
client = TestClient(app)

@app.get("/")
def home():
    return {"hello": "world"}

@app.post("/chat/{chat_id}")
def send_message(chat_id: int, message: Message):
    pass

@app.get("/chat/{chat_id}")
def get_messages(chat_id: int):
    pass

@app.get("/contacts")
def get_contacts():
    pass

@app.post("/chat")
def create_chat():
    pass

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app")