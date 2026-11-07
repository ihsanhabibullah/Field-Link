import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}

class Config:
    APP_NAME = os.getenv("APP_NAME", "FIELDLINK")
    DEBUG = env_bool("DEBUG", False)
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5001"))
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "db_fieldlink")
    SHARED_API_KEY = os.getenv("SHARED_API_KEY", "")
    ACTRACE_API_URL = os.getenv("ACTRACE_API_URL", "").rstrip("/")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", False)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    @classmethod
    def validate(cls):
        if len(cls.SECRET_KEY) < 32:
            raise RuntimeError("SECRET_KEY FIELDLINK wajib minimal 32 karakter.")