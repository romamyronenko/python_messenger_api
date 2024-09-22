from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from app import security
from models import models
from app.security import UserCreate, get_user, create_user, get_db, verify_password, create_access_token, get_current_user

auth_router = APIRouter(prefix='/auth', tags=['authentication'])


@auth_router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    fields_to_check = {"username": user.username, "email": user.email}

    for field, value in fields_to_check.items():
        db_user = get_user(db, **{field: value})
        if db_user:
            raise HTTPException(status_code=400, detail=f"{field.capitalize()} already registered")

    new_user = create_user(db, user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@auth_router.post("/login")
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

@auth_router.get("/users/me")
async def read_users_me(current_user: models.UserDB = Depends(get_current_user)):
    return current_user