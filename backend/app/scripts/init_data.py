import asyncio
import os
import sys
from datetime import date
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from app.database.session import engine, create_db_and_tables
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.teacher import Teacher
from app.auth.token import get_password_hash

async def create_default_admin():
    """Create a default admin user if no admin exists"""
    print("Creating default admin user if none exists...")
    
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if any admin user exists
        admin = session.exec(select(User).where(User.role == UserRole.ADMIN)).first()
        
        if admin:
            print(f"Admin user already exists: {admin.email}")
            return
        
        # Create default admin
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@school.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "adminpassword")
        
        admin = User(
            email=admin_email,
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            hashed_password=get_password_hash(admin_password)
        )
        
        session.add(admin)
        session.commit()
        session.refresh(admin)
        
        print(f"Created default admin user: {admin.email}")

async def create_sample_data():
    """Create some sample data for testing purposes"""
    print("Creating sample data if none exists...")
    
    with Session(engine) as session:
        # Check if we already have data
        if session.exec(select(User).where(User.email == "teacher@school.com")).first():
            print("Sample data already exists, skipping...")
            return
            
        # Create a teacher user
        teacher_user = User(
            email="teacher@school.com",
            first_name="Teacher",
            last_name="Example",
            role=UserRole.TEACHER,
            hashed_password=get_password_hash("teacherpassword")
        )
        
        session.add(teacher_user)
        session.commit()
        session.refresh(teacher_user)
        
        # Create teacher profile
        teacher = Teacher(
            user_id=teacher_user.id,
            hire_date=date.today(),
            qualification="Ph.D. in Education",
            department="Mathematics"
        )
        
        session.add(teacher)
        
        # Create a student user
        student_user = User(
            email="student@school.com",
            first_name="Student",
            last_name="Example",
            role=UserRole.STUDENT,
            hashed_password=get_password_hash("studentpassword")
        )
        
        session.add(student_user)
        session.commit()
        session.refresh(student_user)
        
        # Create student profile
        student = Student(
            user_id=student_user.id,
            enrollment_date=date.today(),
            grade_level=10,
            parent_name="Parent Example",
            parent_email="parent@example.com"
        )
        
        session.add(student)
        session.commit()
        
        print("Sample data created successfully!")

async def main():
    await create_default_admin()
    
    # Optional: Create sample data
    if os.environ.get("CREATE_SAMPLE_DATA", "false").lower() == "true":
        await create_sample_data()

if __name__ == "__main__":
    asyncio.run(main())