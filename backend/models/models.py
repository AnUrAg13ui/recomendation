import uuid
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password_hash = Column(Text)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    roadmaps = relationship("UserRoadmap", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    experience_level = Column(String)
    current_skills = Column(JSONB)
    career_goal = Column(String)
    preferred_stack = Column(JSONB)
    daily_study_hours = Column(Integer)
    target_months = Column(Integer)

    user = relationship("User", back_populates="profile")

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    is_ai_generated = Column(Boolean, default=False)
    category = Column(String)
    roadmap_data = Column(JSONB)
    estimated_weeks = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_roadmaps = relationship("UserRoadmap", back_populates="roadmap")
    progress_entries = relationship("UserProgress", back_populates="roadmap")

class UserRoadmap(Base):
    __tablename__ = "user_roadmaps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    roadmap_id = Column(UUID(as_uuid=True), ForeignKey("roadmaps.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    progress_percentage = Column(Float, default=0.0)
    status = Column(String, default="active") # active, completed, abandoned

    user = relationship("User", back_populates="roadmaps")
    roadmap = relationship("Roadmap", back_populates="user_roadmaps")

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    roadmap_id = Column(UUID(as_uuid=True), ForeignKey("roadmaps.id"))
    topic_name = Column(String)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progress")
    roadmap = relationship("Roadmap", back_populates="progress_entries")
