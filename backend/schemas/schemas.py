from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class UserProfileCreate(BaseModel):
    experience_level: str
    current_skills: List[str]
    career_goal: str
    preferred_stack: List[str]
    daily_study_hours: int
    target_months: int

class UserProfileResponse(UserProfileCreate):
    id: UUID
    user_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class RoadmapPhaseTopic(BaseModel):
    phase: str
    topics: List[str]
    project: str

class RoadmapData(BaseModel):
    phases: List[RoadmapPhaseTopic]

class RoadmapResponse(BaseModel):
    id: UUID
    title: str
    is_ai_generated: bool
    category: Optional[str] = None
    roadmap_data: dict
    estimated_weeks: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserRoadmapResponse(BaseModel):
    id: UUID
    user_id: UUID
    roadmap_id: UUID
    started_at: datetime
    progress_percentage: float
    status: str
    
    model_config = ConfigDict(from_attributes=True)
