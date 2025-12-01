# src/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    BACKEND_URL: str
    FRONTEND_URL: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # This tells Pydantic to read from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

config = Config()