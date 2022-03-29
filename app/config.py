import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = os.environ.getenv("DATABASE_HOSTNAME")
    database_port: str = os.environ.getenv("DATABASE_PORT")
    database_password: str = os.environ.getenv("DATABASE_PORT")
    database_username: str = os.environ.getenv("DATABASE_USERNAME")
    database_name: str = os.environ.getenv("DATABASE_NAME")
    secret_key: str = os.environ.getenv("SECRET_KEY")
    algorithm: str = os.environ.getenv("ALGORITHM")
    access_token_expire_minutes: int = os.environ.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
