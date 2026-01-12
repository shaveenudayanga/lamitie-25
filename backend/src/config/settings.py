from pydantic import BaseSettings

class Settings(BaseSettings):
    db_url: str
    mail_username: str
    mail_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()