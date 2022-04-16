from pydantic import BaseSettings

# Define the settings class
# Use pydantic to validate the settings
# https://pydantic-docs.helpmanual.io/usage/settings/
# Represents the settings for the application
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
