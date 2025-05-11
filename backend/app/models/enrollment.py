from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from .base import BaseModel

class EnrollmentStatus(str, Enum):
    ACTIVE = "active"
    DROPPED = "dropped"
    COMPLETED = "completed"
    PENDING = "pending"

class EnrollmentBase(SQLModel):
    student_id: str = Field(foreign_key="students.id")
    course_id: str = Field(foreign_key="courses.id")
    enrollment_date: date = Field(default_factory=date.today)
    status: EnrollmentStatus = EnrollmentStatus.PENDING

class Enrollment(BaseModel, EnrollmentBase, table=True):
    __tablename__ = "enrollments"
    
    student: "Student" = Relationship(back_populates="enrollments")
    course: "Course" = Relationship(back_populates="enrollments")
    grades: List["Grade"] = Relationship(back_populates="enrollment")

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentRead(EnrollmentBase):
    id: str
    created_at: datetime
    updated_at: datetime

class EnrollmentUpdate(SQLModel):
    status: Optional[EnrollmentStatus] = None