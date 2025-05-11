from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta
from typing import Any
from pydantic import BaseModel

from ..auth.token import create_access_token, verify_password, get_password_hash
from ..auth.dependencies import authenticate_user, get_current_active_user
from ..models.user import User, UserCreate, UserRead
from ..database.session import get_db
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Any

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )
    
    # Exclude sensitive information from user object
    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "is_active": user.is_active
    }
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_data
    }

@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change the password for the current user"""
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password",
        )
    
    # Update password
    hashed_password = get_password_hash(password_data.new_password)
    current_user.hashed_password = hashed_password
    
    db.add(current_user)
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/me", response_model=UserRead)
def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current user information
    """
    return current_user