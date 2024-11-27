from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Document Authenticity Analyzer"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Model paths
    HANDWRITING_MODEL_PATH: str = "models/handwriting_model.pt"
    TEXT_MODEL_PATH: str = "models/text_model.pt"
    
    class Config:
        case_sensitive = True

settings = Settings()