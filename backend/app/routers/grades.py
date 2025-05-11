from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from ..auth.dependencies import get_current_active_user
from ..models.user import User, UserRole
from ..models.grade import Grade, GradeCreate, GradeRead, GradeUpdate, GradeType
from ..models.enrollment import Enrollment, EnrollmentStatus
from ..models.teacher import Teacher
from ..models.student import Student
from ..models.course import Course
from ..database.session import get_db

router = APIRouter(prefix="/grades", tags=["Grades"])

@router.post("/", response_model=GradeRead, status_code=status.HTTP_201_CREATED)
def create_grade(
    *,
    grade_in: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Grade:
    """
    Create a new grade. Only teachers who teach the course or admins can create grades.
    """
    # Check if enrollment exists and is active
    enrollment = db.exec(select(Enrollment).where(Enrollment.id == grade_in.enrollment_id)).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with ID {grade_in.enrollment_id} not found"
        )
    
    if enrollment.status != EnrollmentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add grades to inactive enrollments"
        )
    
    # Get the course for permission check
    course = db.exec(select(Course).where(Course.id == enrollment.course_id)).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.TEACHER:
        # Check if teacher is assigned to this course
        teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if not teacher or teacher.id != course.teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teachers can only add grades to courses they teach"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Validate score
    if grade_in.score < 0 or grade_in.score > grade_in.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Score must be between 0 and {grade_in.max_score}"
        )
    
    # Create the grade
    db_grade = Grade(**grade_in.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/", response_model=List[GradeRead])
def read_grades(
    *,
    skip: int = 0,
    limit: int = 100,
    enrollment_id: Optional[str] = None,
    grade_type: Optional[GradeType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Grade]:
    """
    Retrieve grades. Can be filtered by enrollment_id and grade_type.
    Students can only see their own grades.
    """
    query = select(Grade)
    
    # Apply filters
    if enrollment_id:
        query = query.where(Grade.enrollment_id == enrollment_id)
    
    if grade_type:
        query = query.where(Grade.grade_type == grade_type)
    
    # Handle permissions for students
    if current_user.role == UserRole.STUDENT:
        # Students can only see their own grades
        student = db.exec(select(Student).where(Student.user_id == current_user.id)).first()
        if not student:
            return []
        
        # Find student's enrollments
        student_enrollments = db.exec(
            select(Enrollment.id).where(Enrollment.student_id == student.id)
        ).all()
        
        if not student_enrollments:
            return []
        
        enrollment_ids = [enrollment.id for enrollment in student_enrollments]
        query = query.where(Grade.enrollment_id.in_(enrollment_ids))
    
    grades = db.exec(query.offset(skip).limit(limit)).all()
    return grades

@router.get("/{grade_id}", response_model=GradeRead)
def read_grade(
    *,
    grade_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Grade:
    """
    Get a specific grade by ID.
    """
    grade = db.exec(select(Grade).where(Grade.id == grade_id)).first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grade with ID {grade_id} not found"
        )
    
    # Check permissions for students
    if current_user.role == UserRole.STUDENT:
        # Get the enrollment
        enrollment = db.exec(select(Enrollment).where(Enrollment.id == grade.enrollment_id)).first()
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Check if the student is the owner of this grade
        student = db.exec(select(Student).where(Student.user_id == current_user.id)).first()
        if not student or student.id != enrollment.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only view their own grades"
            )
    
    return grade

@router.patch("/{grade_id}", response_model=GradeRead)
def update_grade(
    *,
    grade_id: str,
    grade_in: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Grade:
    """
    Update a grade. Only teachers of the course or admins can update grades.
    """
    grade = db.exec(select(Grade).where(Grade.id == grade_id)).first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grade with ID {grade_id} not found"
        )
    
    # Get the enrollment and course for permission check
    enrollment = db.exec(select(Enrollment).where(Enrollment.id == grade.enrollment_id)).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    course = db.exec(select(Course).where(Course.id == enrollment.course_id)).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.TEACHER:
        # Check if teacher is assigned to this course
        teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if not teacher or teacher.id != course.teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teachers can only update grades for courses they teach"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Validate score if provided
    grade_data = grade_in.dict(exclude_unset=True)
    if "score" in grade_data:
        if grade_data["score"] < 0 or grade_data["score"] > grade.max_score:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Score must be between 0 and {grade.max_score}"
            )
    
    # Update grade
    for key, value in grade_data.items():
        setattr(grade, key, value)
    
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    *,
    grade_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a grade. Only admin users or the teacher of the course can delete grades.
    """
    grade = db.exec(select(Grade).where(Grade.id == grade_id)).first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grade with ID {grade_id} not found"
        )
    
    # Get the enrollment and course for permission check
    enrollment = db.exec(select(Enrollment).where(Enrollment.id == grade.enrollment_id)).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    course = db.exec(select(Course).where(Course.id == enrollment.course_id)).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.TEACHER:
        # Check if teacher is assigned to this course
        teacher = db.exec(select(Teacher).where(Teacher.user_id == current_user.id)).first()
        if not teacher or teacher.id != course.teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teachers can only delete grades for courses they teach"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(grade)
    db.commit()
    return None