from fastapi import FastAPI, Depends, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient
from app.authorization import auth_router
from app.security import get_current_user
from models import models
from models.database import engine
from models.message import Message

models.Base.metadata.create_all(bind=engine)

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app")