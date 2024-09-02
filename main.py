from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import models, database
from models.database import engine
from security import UserCreate, get_db, create_user, get_user, get_current_user, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Message(BaseModel):
    content: str

@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = get_user(db, username=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: models.UserDB = Depends(get_current_user)):
    return current_user

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