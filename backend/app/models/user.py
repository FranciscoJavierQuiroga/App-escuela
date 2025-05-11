from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from datetime import datetime
from .base import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool = True

class User(BaseModel, UserBase, table=True):
    __tablename__ = "users"
    
    hashed_password: str
    
    # Relationships
    student: Optional["Student"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    teacher: Optional["Teacher"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None