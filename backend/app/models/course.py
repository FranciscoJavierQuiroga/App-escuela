from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, ForwardRef
from datetime import datetime, date
from enum import Enum
from .base import BaseModel

class CourseStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    UPCOMING = "upcoming"

class CourseBase(SQLModel):
    name: str
    description: Optional[str] = None
    code: str = Field(unique=True)
    credit_hours: int
    teacher_id: str = Field(foreign_key="teachers.id")
    max_students: int = 30
    start_date: date
    end_date: date
    status: CourseStatus = CourseStatus.UPCOMING

class Course(BaseModel, CourseBase, table=True):
    __tablename__ = "courses"
    
    teacher: "Teacher" = Relationship(back_populates="courses")
    enrollments: List["Enrollment"] = Relationship(back_populates="course")

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: str
    created_at: datetime
    updated_at: datetime

class CourseUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    credit_hours: Optional[int] = None
    teacher_id: Optional[str] = None
    max_students: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[CourseStatus] = None