from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_VERSION: str = "0.0.1"

    class Config:
        env_file = ".env"


config = Config()
