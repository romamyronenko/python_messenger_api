from typing import ClassVar

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_VERSION: str = "0.0.1"
    SECRET_KEY: ClassVar[str] = "your_secret_key"
    ALGORITHM: ClassVar[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: ClassVar[int] = 30

    class Config:
        env_file = ".env"


config = Config()
