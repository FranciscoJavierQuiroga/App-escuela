from .base import BaseModel
from .user import User, UserCreate, UserRead, UserUpdate, UserRole
from .student import Student, StudentCreate, StudentRead, StudentUpdate
from .teacher import Teacher, TeacherCreate, TeacherRead, TeacherUpdate
from .course import Course, CourseCreate, CourseRead, CourseUpdate, CourseStatus
from .enrollment import Enrollment, EnrollmentCreate, EnrollmentRead, EnrollmentUpdate, EnrollmentStatus
from .grade import Grade, GradeCreate, GradeRead, GradeUpdate, GradeType

# For database creation, import all models
__all__ = [
    "BaseModel",
    "User", "UserCreate", "UserRead", "UserUpdate", "UserRole",
    "Student", "StudentCreate", "StudentRead", "StudentUpdate",
    "Teacher", "TeacherCreate", "TeacherRead", "TeacherUpdate", 
    "Course", "CourseCreate", "CourseRead", "CourseUpdate", "CourseStatus",
    "Enrollment", "EnrollmentCreate", "EnrollmentRead", "EnrollmentUpdate", "EnrollmentStatus",
    "Grade", "GradeCreate", "GradeRead", "GradeUpdate", "GradeType"
]