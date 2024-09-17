from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_VERSION: str = "0.0.1"

    class Config:
        env_file = ".env"

class Settings(BaseSettings):
    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


config = Config()
settings = Settings()
