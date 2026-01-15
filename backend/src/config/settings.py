from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    db_url: str
    mail_username: str
    mail_password: str
    allow_origins: List[str] = ["*"]
    
    # Authentication settings
    admin_password: str = "Lam#&faS25"
    jwt_secret_key: str = "lamitie25-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()