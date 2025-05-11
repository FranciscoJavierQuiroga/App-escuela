from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from ..auth.dependencies import get_current_active_user
from ..models.user import User, UserRole
from ..models.enrollment import Enrollment, EnrollmentCreate, EnrollmentRead, EnrollmentUpdate, EnrollmentStatus
from ..models.student import Student
from ..models.course import Course, CourseStatus
from ..database.session import get_db

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    *,
    enrollment_in: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Enrollment:
    """
    Create a new enrollment. Admin users can create any enrollment.
    Students can only enroll themselves in active courses.
    """
    # Check if student exists
    student = db.exec(select(Student).where(Student.id == enrollment_in.student_id)).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {enrollment_in.student_id} not found"
        )
    
    # Check if course exists and is active
    course = db.exec(select(Course).where(Course.id == enrollment_in.course_id)).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {enrollment_in.course_id} not found"
        )
    
    if course.status != CourseStatus.ACTIVE and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot enroll in a course that is not active"
        )
    
    # Check permissions
    if current_user.role == UserRole.STUDENT:
        # Students can only enroll themselves
        student_profile = db.exec(select(Student).where(Student.user_id == current_user.id)).first()
        if not student_profile or student_profile.id != enrollment_in.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only enroll themselves"
            )
    elif current_user.role not in [UserRole.ADMIN, UserRole.TEACHER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if enrollment already exists
    existing_enrollment = db.exec(
        select(Enrollment).where(
            Enrollment.student_id == enrollment_in.student_id,
            Enrollment.course_id == enrollment_in.course_id
        )
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student is already enrolled in this course"
        )
    
    # Check if course has reached maximum capacity
    current_enrollments = db.exec(
        select(Enrollment).where(
            Enrollment.course_id == enrollment_in.course_id,
            Enrollment.status.in_([EnrollmentStatus.ACTIVE, EnrollmentStatus.PENDING])
        )
    ).all()
    
    if len(current_enrollments) >= course.max_students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course has reached maximum capacity"
        )
    
    # Create new enrollment
    db_enrollment = Enrollment(**enrollment_in.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/", response_model=List[EnrollmentRead])
def read_enrollments(
    *,
    skip: int = 0,
    limit: int = 100,
    student_id: Optional[str] = None,
    course_id: Optional[str] = None,
    status: Optional[EnrollmentStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Enrollment]:
    """
    Retrieve enrollments. Can be filtered by student_id, course_id, and status.
    Students can only see their own enrollments.
    """
    query = select(Enrollment)
    
    # Apply filters
    if student_id:
        query = query.where(Enrollment.student_id == student_id)
    
    if course_id:
        query = query.where(Enrollment.course_id == course_id)
    
    if status:
        query = query.where(Enrollment.status == status)
    
    # Handle permissions
    if current_user.role == UserRole.STUDENT:
        # Students can only see their own enrollments
        student = db.exec(select(Student).where(Student.user_id == current_user.id)).first()
        if not student:
            return []
        query = query.where(Enrollment.student_id == student.id)
    
    enrollments = db.exec(query.offset(skip).limit(limit)).all()
    return enrollments

@router.get("/{enrollment_id}", response_model=EnrollmentRead)
def read_enrollment(
    *,
    enrollment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Enrollment:
    """
    Get a specific enrollment by ID.
    """
    enrollment = db.exec(select(Enrollment).where(Enrollment.id == enrollment_id)).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with ID {enrollment_id} not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.STUDENT:
        # Students can only see their own enrollments
        student = db.exec(select(Student).where(Student.user_id == current_user.id)).first()
        if not student or student.id != enrollment.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return enrollment

@router.patch("/{enrollment_id}", response_model=EnrollmentRead)
def update_enrollment(
    *,
    enrollment_id: str,
    enrollment_in: EnrollmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Enrollment:
    """
    Update an enrollment status. Admin and teachers can update any enrollment.
    Students can only drop (cancel) their own enrollments.
    """
    enrollment = db.exec(select(Enrollment).where(Enrollment.id == enrollment_id)).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with ID {enrollment_id} not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.STUDENT:
        # Students can only update their own enrollments to "DROPPED" status
        student = db.exec(select(Student).where(Student.user_id == current_user.id)).first()
        if not student or student.id != enrollment.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        if enrollment_in.status != EnrollmentStatus.DROPPED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only drop enrollments"
            )
    
    # Update enrollment status
    enrollment_data = enrollment_in.dict(exclude_unset=True)
    for key, value in enrollment_data.items():
        setattr(enrollment, key, value)
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    *,
    enrollment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete an enrollment. Only admin users can delete enrollments.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    enrollment = db.exec(select(Enrollment).where(Enrollment.id == enrollment_id)).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with ID {enrollment_id} not found"
        )
    
    db.delete(enrollment)
    db.commit()
    return None