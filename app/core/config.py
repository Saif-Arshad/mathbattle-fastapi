from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb+srv://user:e3vJNllvkEl9xPYT@cluster0.dpyt0g3.mongodb.net"
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
