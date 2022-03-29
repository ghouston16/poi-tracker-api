import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = os.environ.get("DATABASE_HOSTNAME")
    database_port: str = os.environ.get("DATABASE_PORT")
    database_password: str = os.environ.get("DATABASE_PORT")
    database_username: str = os.environ.get("DATABASE_USERNAME")
    database_name: str = os.environ.get("DATABASE_NAME")
    secret_key: str = os.environ.get("SECRET_KEY")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str = os.environ.get("DATABASE_URL")

    class Config:
        env_file = ".env"


settings = Settings()
