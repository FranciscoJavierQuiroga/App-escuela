from sqlmodel import Session, select
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from ..models.student import Student
from ..models.user import User
from ..models.enrollment import Enrollment
from ..models.course import Course
from ..models.grade import Grade
from ..utils.logger import app_logger

# Create reports directory
REPORTS_DIR = Path(__file__).parent.parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

class ReportService:
    """Service for generating various reports related to students and courses."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_student_grades(self, student_id: int) -> Dict[str, Any]:
        """Get all grades for a specific student with course information."""
        # Get student
        student = self.db.get(Student, student_id)
        if not student:
            app_logger.warning(f"Student with ID {student_id} not found")
            return {"error": "Student not found"}
        
        # Get student user info
        user = self.db.get(User, student.user_id)
        
        # Get enrollments for student
        query = (
            select(Enrollment, Course, Grade)
            .join(Course, Enrollment.course_id == Course.id)
            .outerjoin(Grade, (Grade.enrollment_id == Enrollment.id))
            .where(Enrollment.student_id == student_id)
        )
        results = self.db.exec(query).all()
        
        grades_data = []
        for enrollment, course, grade in results:
            grade_value = grade.grade_value if grade else None
            
            grades_data.append({
                "course_id": course.id,
                "course_name": course.name,
                "course_code": course.code,
                "enrollment_date": enrollment.enrollment_date,
                "grade": grade_value,
                "grade_date": grade.grade_date if grade else None,
            })
        
        report_data = {
            "student_id": student_id,
            "student_name": f"{user.first_name} {user.last_name}",
            "grade_level": student.grade_level,
            "enrollment_date": student.enrollment_date,
            "grades": grades_data,
            "generated_at": datetime.now().isoformat(),
        }
        
        app_logger.info(f"Generated grades report for student {student_id}")
        return report_data
    
    def generate_student_transcript_pdf(self, student_id: int) -> str:
        """Generate a PDF transcript for a student."""
        # Get student data
        student_data = self.get_student_grades(student_id)
        
        if "error" in student_data:
            app_logger.error(f"Failed to generate transcript for student {student_id}: {student_data['error']}")
            return None
        
        # Create PDF file
        filename = f"student_{student_id}_transcript_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = REPORTS_DIR / filename
        
        # Create the PDF
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        subtitle_style = styles["Heading2"]
        normal_style = styles["Normal"]
        
        # Build the PDF content
        content = []
        
        # Title
        content.append(Paragraph(f"Academic Transcript", title_style))
        content.append(Spacer(1, 20))
        
        # Student Info
        content.append(Paragraph(f"Student: {student_data['student_name']}", subtitle_style))
        content.append(Paragraph(f"ID: {student_data['student_id']}", normal_style))
        content.append(Paragraph(f"Grade Level: {student_data['grade_level']}", normal_style))
        content.append(Paragraph(f"Enrollment Date: {student_data['enrollment_date']}", normal_style))
        content.append(Spacer(1, 20))
        
        # Grades Table
        if student_data['grades']:
            # Table header
            table_data = [["Course Code", "Course Name", "Grade"]]
            
            # Table data
            for course in student_data['grades']:
                grade = course['grade'] if course['grade'] else "Not graded"
                table_data.append([
                    course['course_code'],
                    course['course_name'],
                    grade
                ])
            
            # Calculate GPA if grades are available
            graded_courses = [c for c in student_data['grades'] if c['grade'] is not None]
            if graded_courses:
                avg_grade = sum(c['grade'] for c in graded_courses) / len(graded_courses)
                table_data.append(["", "Average Grade", f"{avg_grade:.1f}"])
            
            # Create table
            table = Table(table_data, colWidths=[100, 250, 100])
            
            # Style the table
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            content.append(table)
        else:
            content.append(Paragraph("No course records found for this student.", normal_style))
        
        # Footer
        content.append(Spacer(1, 30))
        content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        
        # Build and save the PDF
        doc.build(content)
        
        app_logger.info(f"Generated PDF transcript for student {student_id} at {pdf_path}")
        return str(pdf_path)
    
    def export_all_students_to_excel(self) -> str:
        """Export all students' information to an Excel file."""
        # Query student data with users
        query = (
            select(Student, User)
            .join(User, Student.user_id == User.id)
        )
        results = self.db.exec(query).all()
        
        # Convert to DataFrame
        students_data = []
        for student, user in results:
            students_data.append({
                "student_id": student.id,
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "grade_level": student.grade_level,
                "enrollment_date": student.enrollment_date,
                "parent_name": student.parent_name,
                "parent_email": student.parent_email,
            })
        
        df = pd.DataFrame(students_data)
        
        # Save to Excel
        filename = f"all_students_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        excel_path = REPORTS_DIR / filename
        
        df.to_excel(str(excel_path), index=False, sheet_name="Students")
        
        app_logger.info(f"Exported all students data to Excel: {excel_path}")
        return str(excel_path)
