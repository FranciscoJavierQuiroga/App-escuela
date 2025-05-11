from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from ..auth.dependencies import get_current_active_user
from ..models.user import User, UserRole
from ..models.course import Course, CourseCreate, CourseRead, CourseUpdate, CourseStatus
from ..models.teacher import Teacher
from ..database.session import get_db

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    *,
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Course:
    """
    Create a new course. Only admin users and teachers can create courses.
    """
    # Check permissions
    if current_user.role == UserRole.TEACHER:
        # Teachers can only create courses assigned to themselves
        teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if not teacher or teacher.id != course_in.teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teachers can only create courses for themselves"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if teacher exists
    teacher = db.exec(select(Teacher).where(Teacher.id == course_in.teacher_id)).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with ID {course_in.teacher_id} not found"
        )
    
    # Check if course code already exists
    existing_course = db.exec(select(Course).where(Course.code == course_in.code)).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with code {course_in.code} already exists"
        )
    
    # Create new course
    db_course = Course(**course_in.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=List[CourseRead])
def read_courses(
    *,
    skip: int = 0,
    limit: int = 100,
    status: Optional[CourseStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Course]:
    """
    Retrieve courses. All authenticated users can access this endpoint.
    Filter by status is optional.
    """
    query = select(Course)
    
    # Apply status filter if provided
    if status:
        query = query.where(Course.status == status)
    
    # Apply teacher filter for teachers
    if current_user.role == UserRole.TEACHER:
        teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if teacher:
            query = query.where(Course.teacher_id == teacher.id)
    
    courses = db.exec(query.offset(skip).limit(limit)).all()
    return courses

@router.get("/{course_id}", response_model=CourseRead)
def read_course(
    *,
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Course:
    """
    Get a specific course by ID.
    """
    course = db.exec(select(Course).where(Course.id == course_id)).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    return course

@router.patch("/{course_id}", response_model=CourseRead)
def update_course(
    *,
    course_id: str,
    course_in: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Course:
    """
    Update a course. Admins can update any course, teachers can only update their own courses.
    """
    course = db.exec(select(Course).where(Course.id == course_id)).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.TEACHER:
        # Teachers can only update their own courses
        teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if not teacher or teacher.id != course.teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teachers can only update their own courses"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update course attributes
    course_data = course_in.dict(exclude_unset=True)
    
    # If teacher_id is being updated, verify the teacher exists
    if "teacher_id" in course_data and course_data["teacher_id"] != course.teacher_id:
        teacher = db.exec(select(Teacher).where(Teacher.id == course_data["teacher_id"])).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with ID {course_data['teacher_id']} not found"
            )
    
    # Apply updates
    for key, value in course_data.items():
        setattr(course, key, value)
    
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    *,
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a course. Only admin users can delete courses.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    course = db.exec(select(Course).where(Course.id == course_id)).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    
    db.delete(course)
    db.commit()
    return None