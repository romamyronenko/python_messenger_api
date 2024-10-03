from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

import database.schema
from app.models import (
    UserCreatedResponse,
    TokenResponse,
    UserAuthRequest,
    CurrentUserResponse,
)
from app.security import (
    UserCreate,
    get_user,
    create_user,
    get_db,
    verify_password,
    create_access_token,
    get_current_user,
)
from core.config import config


auth_router = APIRouter(prefix='/auth', tags=['authentication'])


@auth_router.post("/register")
async def register(
    user: UserCreate, db: Session = Depends(get_db)
) -> UserCreatedResponse:
    fields_to_check = {"username": user.username, "email": user.email}

    for field, value in fields_to_check.items():
        db_user = get_user(db, **{field: value})
        if db_user:
            raise HTTPException(
                status_code=400, detail=f"{field.capitalize()} already registered"
            )

    new_user = create_user(db, user)
    return UserCreatedResponse(
        message="User registered successfully", id=new_user.id
    )


@auth_router.post("/login")
async def login(
    form_data: UserAuthRequest, db: Session = Depends(get_db)
) -> TokenResponse:
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me")
async def read_users_me(
    current_user: database.schema.User = Depends(get_current_user),
) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        display_name=current_user.full_name
    )
