from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session
from typing import List
from fastapi.responses import FileResponse
from pathlib import Path
import os
from datetime import datetime

from ..database.session import get_db
from ..services.report_service import ReportService
from ..schemas.reports import StudentGradeReport, ReportResponse
from ..auth.dependencies import get_current_active_user
from ..models.user import User, UserRole
from ..utils.logger import app_logger

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(get_current_active_user)]
)

def get_report_service(db: Session = Depends(get_db)) -> ReportService:
    return ReportService(db)

@router.get("/students/{student_id}/grades", response_model=StudentGradeReport)
def get_student_grades(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    report_service: ReportService = Depends(get_report_service)
):
    """Get grades report for a specific student."""
    # Check permissions - admin, teacher, or the student themselves
    if (current_user.role != UserRole.ADMIN and 
        current_user.role != UserRole.TEACHER and
        (current_user.role == UserRole.STUDENT and current_user.student[0].id != student_id)):
        app_logger.warning(f"User {current_user.id} tried to access grades for student {student_id} without permission")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this student's grades"
        )
    
    report = report_service.get_student_grades(student_id)
    
    if "error" in report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=report["error"]
        )
    
    return report

@router.get("/students/{student_id}/transcript")
def generate_student_transcript(
    student_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    report_service: ReportService = Depends(get_report_service)
):
    """Generate a PDF transcript for a student."""
    # Check permissions - admin, teacher, or the student themselves
    if (current_user.role != UserRole.ADMIN and 
        current_user.role != UserRole.TEACHER and
        (current_user.role == UserRole.STUDENT and current_user.student[0].id != student_id)):
        app_logger.warning(f"User {current_user.id} tried to generate transcript for student {student_id} without permission")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to generate this student's transcript"
        )
    
    # Generate the PDF
    pdf_path = report_service.generate_student_transcript_pdf(student_id)
    
    if not pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to generate transcript - student not found"
        )
    
    return FileResponse(
        path=pdf_path,
        filename=Path(pdf_path).name,
        media_type="application/pdf"
    )

@router.get("/export/students", response_model=ReportResponse)
def export_all_students(
    current_user: User = Depends(get_current_active_user),
    report_service: ReportService = Depends(get_report_service)
):
    """Export all students to Excel (admin and teachers only)."""
    # Check permissions - admin or teacher only
    if current_user.role not in [UserRole.ADMIN, UserRole.TEACHER]:
        app_logger.warning(f"User {current_user.id} tried to export all students without permission")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators and teachers can export all students"
        )
    
    # Generate the Excel file
    excel_path = report_service.export_all_students_to_excel()
    filename = Path(excel_path).name
    
    return {
        "filename": filename,
        "file_path": excel_path,
        "generated_at": datetime.now(),
        "file_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
