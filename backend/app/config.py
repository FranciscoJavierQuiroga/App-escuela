from pydantic import BaseSettings, validator
from typing import List, Optional, Union
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the path to the .env file
env_path = Path(__file__).parent / ".env"
# Load environment variables from .env file if it exists
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """Application settings."""
    
    APP_NAME: str = "School Management System"
    DEBUG: bool = True
    
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/school_management"
    TEST_DATABASE_URL: Optional[str] = "postgresql://postgres:postgres@db:5432/test_school_management"
    
    # Security settings
    SECRET_KEY: str = "your_super_secret_key_here_please_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Admin settings
    CREATE_SAMPLE_DATA: bool = False
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global instance of settings
settings = Settings()