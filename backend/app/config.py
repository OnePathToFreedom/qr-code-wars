import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Базовые настройки
    PROJECT_NAME: str = "QR Code Wars"
    API_V1_STR: str = "/api/v1"
    
    # Секретный ключ для генерации JWT и других данных
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key_for_development_only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    
    # Соль для генерации QR-кодов
    QR_SECRET_SALT: str = os.getenv("QR_SECRET_SALT", "qr_secret_salt_for_development")
    
    # Настройки базы данных - используем SQLite
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./qrcodewars.db"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 