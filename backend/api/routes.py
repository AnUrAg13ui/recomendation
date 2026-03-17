from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from backend.database import get_db
from backend.models import models
from backend.schemas import schemas
from backend.services.roadmap_engine.pipeline import roadmap_engine

router = APIRouter()

@router.post("/generate-roadmap", response_model=schemas.RoadmapResponse)
def generate_roadmap(profile_data: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    """
    Receives user profile, generates roadmap via AI, stores roadmap and profile, 
    and returns the structured roadmap JSON.
    """
    try:
        # Create or fetch user
        # In a real app we'd handle auth. Here we use a mock user for the session.
        mock_user = db.query(models.User).filter(models.User.email == "test@example.com").first()
        if not mock_user:
            mock_user = models.User(email="test@example.com", full_name="Test User", password_hash="dummy")
            db.add(mock_user)
            db.commit()
            db.refresh(mock_user)

        # Create Profile
        user_profile = models.UserProfile(
            user_id=mock_user.id,
            experience_level=profile_data.experience_level,
            current_skills=profile_data.current_skills,
            career_goal=profile_data.career_goal,
            preferred_stack=profile_data.preferred_stack,
            daily_study_hours=profile_data.daily_study_hours,
            target_months=profile_data.target_months
        )
        db.add(user_profile)
        
        # Generate Roadmap
        roadmap_json = roadmap_engine.generate_roadmap(profile_data)
        
        # Determine Estimated Weeks
        # Optionally parse from roadmap or default
        estimated_weeks = profile_data.target_months * 4
        
        # Store Roadmap
        new_roadmap = models.Roadmap(
            title=f"{profile_data.career_goal} Roadmap",
            is_ai_generated=True,
            category="custom",
            roadmap_data=roadmap_json,
            estimated_weeks=estimated_weeks
        )
        db.add(new_roadmap)
        db.commit()
        db.refresh(new_roadmap)
        
        # Associate User to Roadmap
        user_roadmap = models.UserRoadmap(
            user_id=mock_user.id,
            roadmap_id=new_roadmap.id
        )
        db.add(user_roadmap)
        db.commit()
        
        return new_roadmap
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roadmaps", response_model=List[schemas.RoadmapResponse])
def get_roadmaps(db: Session = Depends(get_db)):
    roadmaps = db.query(models.Roadmap).all()
    return roadmaps

@router.get("/user-roadmaps", response_model=List[schemas.UserRoadmapResponse])
def get_user_roadmaps(db: Session = Depends(get_db), user_id: UUID = None):
    query = db.query(models.UserRoadmap)
    if user_id:
        query = query.filter(models.UserRoadmap.user_id == user_id)
    return query.all()
