from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from ..auth.dependencies import get_current_active_user
from ..models.user import User, UserRole
from ..models.student import Student, StudentCreate, StudentRead, StudentUpdate
from ..database.session import get_db

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    *,
    student_in: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Student:
    """
    Create a new student profile. Only admin users can create student profiles.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if user exists
    user = db.exec(select(User).where(User.id == student_in.user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {student_in.user_id} not found"
        )
    
    # Check if user already has a student profile
    existing_student = db.exec(select(Student).where(Student.user_id == student_in.user_id)).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already has a student profile"
        )
    
    # Create new student profile
    db_student = Student(**student_in.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/", response_model=List[StudentRead])
def read_students(
    *,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Student]:
    """
    Retrieve students. Teachers and admins can access this endpoint.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.TEACHER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    students = db.exec(select(Student).offset(skip).limit(limit)).all()
    return students

@router.get("/{student_id}", response_model=StudentRead)
def read_student(
    *,
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Student:
    """
    Get a specific student by ID.
    """
    # Students can only access their own record
    if current_user.role == UserRole.STUDENT:
        student = db.exec(select(Student).where(Student.user_id == current_user.id)).first()
        if not student or student.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    student = db.exec(select(Student).where(Student.id == student_id)).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return student

@router.patch("/{student_id}", response_model=StudentRead)
def update_student(
    *,
    student_id: str,
    student_in: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Student:
    """
    Update a student. Only admins can update student profiles.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    student = db.exec(select(Student).where(Student.id == student_id)).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    
    # Update student attributes
    student_data = student_in.dict(exclude_unset=True)
    for key, value in student_data.items():
        setattr(student, key, value)
    
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    *,
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a student profile. Only admin users can delete student profiles.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    student = db.exec(select(Student).where(Student.id == student_id)).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    
    db.delete(student)
    db.commit()
    return None