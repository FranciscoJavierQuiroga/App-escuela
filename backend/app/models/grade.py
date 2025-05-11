from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from .base import BaseModel

class GradeType(str, Enum):
    EXAM = "exam"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    PROJECT = "project"
    PARTICIPATION = "participation"
    FINAL = "final"

class GradeBase(SQLModel):
    enrollment_id: str = Field(foreign_key="enrollments.id")
    grade_type: GradeType
    score: float
    max_score: float
    weight: float  # Percentage weight in final grade
    comments: Optional[str] = None
    grade_date: date = Field(default_factory=date.today)

class Grade(BaseModel, GradeBase, table=True):
    __tablename__ = "grades"
    
    enrollment: "Enrollment" = Relationship(back_populates="grades")

class GradeCreate(GradeBase):
    pass

class GradeRead(GradeBase):
    id: str
    created_at: datetime
    updated_at: datetime

class GradeUpdate(SQLModel):
    score: Optional[float] = None
    comments: Optional[str] = None