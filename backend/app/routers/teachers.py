from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from ..auth.dependencies import get_current_active_user
from ..models.user import User, UserRole
from ..models.teacher import Teacher, TeacherCreate, TeacherRead, TeacherUpdate
from ..database.session import get_db

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("/", response_model=TeacherRead, status_code=status.HTTP_201_CREATED)
def create_teacher(
    *,
    teacher_in: TeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Teacher:
    """
    Create a new teacher profile. Only admin users can create teacher profiles.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if user exists
    user = db.exec(select(User).where(User.id == teacher_in.user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {teacher_in.user_id} not found"
        )
    
    # Check if user already has a teacher profile
    existing_teacher = db.exec(select(Teacher).where(Teacher.user_id == teacher_in.user_id)).first()
    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already has a teacher profile"
        )
    
    # Create new teacher profile
    db_teacher = Teacher(**teacher_in.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/", response_model=List[TeacherRead])
def read_teachers(
    *,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Teacher]:
    """
    Retrieve teachers. All authenticated users can access this endpoint.
    """
    teachers = db.exec(select(Teacher).offset(skip).limit(limit)).all()
    return teachers

@router.get("/{teacher_id}", response_model=TeacherRead)
def read_teacher(
    *,
    teacher_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Teacher:
    """
    Get a specific teacher by ID.
    """
    # Teachers can only access their own record in detail
    if current_user.role == UserRole.TEACHER:
        teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if not teacher or teacher.id != teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    teacher = db.exec(select(Teacher).where(Teacher.id == teacher_id)).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with ID {teacher_id} not found"
        )
    return teacher

@router.patch("/{teacher_id}", response_model=TeacherRead)
def update_teacher(
    *,
    teacher_id: str,
    teacher_in: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Teacher:
    """
    Update a teacher. Only admins can update all teacher profiles, teachers can update their own profile.
    """
    teacher = db.exec(select(Teacher).where(Teacher.id == teacher_id)).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with ID {teacher_id} not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.TEACHER:
        # Teachers can only update their own profile
        current_teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if not current_teacher or current_teacher.id != teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update teacher attributes
    teacher_data = teacher_in.dict(exclude_unset=True)
    for key, value in teacher_data.items():
        setattr(teacher, key, value)
    
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(
    *,
    teacher_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a teacher profile. Only admin users can delete teacher profiles.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    teacher = db.exec(select(Teacher).where(Teacher.id == teacher_id)).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with ID {teacher_id} not found"
        )
    
    db.delete(teacher)
    db.commit()
    return None