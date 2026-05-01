from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./reciclap.db"
    SECRET_KEY: str = "cambiar-por-clave-secreta"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    UPLOAD_DIR: str = "uploads/evidencias"

    class Config:
        env_file = ".env"

settings = Settings()