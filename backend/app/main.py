from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import time

from .config import settings
from .database.session import create_db_and_tables
from .routers import auth, users, students, teachers, courses, enrollments, grades, reports
from .utils.logger import app_logger

app = FastAPI(
    title=settings.APP_NAME,
    description="API for School Management System",
    version="0.1.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all database tables at startup
@app.on_event("startup")
def on_startup():
    app_logger.info("Starting up application")
    create_db_and_tables()
    app_logger.info("Database tables initialized")

@app.on_event("shutdown")
def on_shutdown():
    app_logger.info("Shutting down application")

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request details and response time."""
    start_time = time.time()
    
    # Get request details
    method = request.method
    url = request.url.path
    
    app_logger.info(f"Request: {method} {url}")
    
    # Process the request
    response = await call_next(request)
    
    # Calculate and log processing time
    process_time = time.time() - start_time
    app_logger.info(f"Response: {method} {url} - Status: {response.status_code} - Time: {process_time:.4f}s")
    
    return response

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(grades.router)
app.include_router(reports.router)  # Ensure this router is included

@app.get("/")
def root():
    app_logger.debug("Root endpoint called")
    return {"message": f"Welcome to {settings.APP_NAME} API"}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    app_logger.debug("Health check endpoint called")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": app.version,
        "environment": "development" if settings.DEBUG else "production"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# For Vercel serverless deployment
handler = app