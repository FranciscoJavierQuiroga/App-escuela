from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, ForwardRef
from datetime import datetime, date
from .base import BaseModel
from .user import User

class StudentBase(SQLModel):
    user_id: str = Field(foreign_key="users.id")
    enrollment_date: date
    grade_level: int
    parent_name: Optional[str] = None
    parent_email: Optional[str] = None
    parent_phone: Optional[str] = None
    address: Optional[str] = None

class Student(BaseModel, StudentBase, table=True):
    __tablename__ = "students"
    
    user: User = Relationship(back_populates="student")
    enrollments: List["Enrollment"] = Relationship(back_populates="student")

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: str
    created_at: datetime
    updated_at: datetime

class StudentUpdate(SQLModel):
    grade_level: Optional[int] = None
    parent_name: Optional[str] = None
    parent_email: Optional[str] = None
    parent_phone: Optional[str] = None
    address: Optional[str] = None