from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Roadmap Recommendation System"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/roadmap_db"
    MODEL_PROVIDER: str = "api"  # "api" or "local"
    
    # API Variables (e.g. Gemini)
    GEMINI_API_KEY: str = "AIzaSyCbIIZeGe9ma1ZMcr5WkSBZlXm-zK1BQKo"
    
    # Local Model Variables (e.g. Ollama endpoint)
    LOCAL_MODEL_URL: str = "http://localhost:11434/api/generate"
    LOCAL_MODEL_NAME: str = "mistral"
    
    class Config:
        env_file = ".env"

settings = Settings()
