import sys
from pathlib import Path

# Add the parent directory to sys.path to allow running from inside backend/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from backend.api import routes
from backend.database import engine
from backend.models import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Roadmap Recommendation System",
    description="Generates personalized learning roadmaps based on user profiles.",
    version="1.0.0"
)

app.include_router(routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AI Roadmap Recommendation System API is running."}
