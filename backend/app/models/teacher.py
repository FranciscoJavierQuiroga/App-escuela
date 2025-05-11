from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, ForwardRef
from datetime import datetime, date
from .base import BaseModel
from .user import User

class TeacherBase(SQLModel):
    user_id: str = Field(foreign_key="users.id")
    hire_date: date
    department: Optional[str] = None
    qualification: str
    phone_number: Optional[str] = None
    bio: Optional[str] = None

class Teacher(BaseModel, TeacherBase, table=True):
    __tablename__ = "teachers"
    
    user: User = Relationship(back_populates="teacher")
    courses: List["Course"] = Relationship(back_populates="teacher")

class TeacherCreate(TeacherBase):
    pass

class TeacherRead(TeacherBase):
    id: str
    created_at: datetime
    updated_at: datetime

class TeacherUpdate(SQLModel):
    department: Optional[str] = None
    qualification: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None