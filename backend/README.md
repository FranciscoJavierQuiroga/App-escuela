# School Management System

A comprehensive web application for managing school operations including students, teachers, courses, enrollments, and grades.

## Features

- User authentication and role-based access control (Admin, Teacher, Student)
- Student management
- Teacher management
- Course management
- Enrollment system
- Grading system

## Backend Technologies

- FastAPI - High-performance web framework
- SQLModel - ORM for database interaction
- PostgreSQL - Database
- JWT Authentication - For secure user authentication

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository
2. Navigate to the backend directory:
   ```
   cd backend
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the backend directory with the following variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/school_management
   SECRET_KEY=your_secure_secret_key
   ```

### Running the Application

Start the backend server:
```
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

The API includes the following main endpoints:

- `/auth` - Authentication endpoints
- `/users` - User management
- `/students` - Student management
- `/teachers` - Teacher management
- `/courses` - Course management
- `/enrollments` - Enrollment management
- `/grades` - Grade management

## Development

### Database Migrations

This project uses Alembic for database migrations. To create a new migration:

```
alembic revision --autogenerate -m "Description of the migration"
```

To apply migrations:

```
alembic upgrade head
```