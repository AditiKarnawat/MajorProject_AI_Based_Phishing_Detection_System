import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Phishing Detection System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Secret Key & Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "phishing-detector-super-secret-key-change-in-production-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/phishing_guard.db")
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]
    
    # Model Artifacts Path
    MODEL_DIR: str = "./models_store"
    DATA_DIR: str = "./data"
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
