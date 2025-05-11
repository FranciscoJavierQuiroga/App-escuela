from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class GradeInfo(BaseModel):
    course_id: int
    course_name: str
    course_code: str
    enrollment_date: date
    grade: Optional[float] = None
    grade_date: Optional[date] = None
    
class StudentGradeReport(BaseModel):
    student_id: int
    student_name: str
    grade_level: int
    enrollment_date: date
    grades: List[GradeInfo]
    generated_at: datetime
    
class ReportResponse(BaseModel):
    filename: str
    file_path: str
    generated_at: datetime
    file_type: str
