from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    BACKEND_URL: str
    FRONTEND_URL: str

    # This tells Pydantic to read from the .env file
    model_config = SettingsConfigDict(env_file="client/.env", env_ignore_empty=True)

settings = Settings()