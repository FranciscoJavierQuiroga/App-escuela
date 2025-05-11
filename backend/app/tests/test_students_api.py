import pytest
from fastapi.testclient import TestClient
import json

def get_auth_header(test_client, email="admin@test.com", password="testpassword"):
    """Helper function to get authentication header"""
    login_data = {
        "username": email,
        "password": password
    }
    
    response = test_client.post("/auth/token", data=login_data)
    data = response.json()
    return {"Authorization": f"Bearer {data['access_token']}"}

def test_get_students(test_client, admin_user):
    """Test retrieving student list"""
    headers = get_auth_header(test_client)
    response = test_client.get("/students/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_student(test_client, admin_user):
    """Test creating a new student"""
    headers = get_auth_header(test_client)
    
    # Create a new user first
    user_data = {
        "email": "newstudent@example.com",
        "first_name": "New",
        "last_name": "Student",
        "password": "password123",
        "role": "STUDENT"
    }
    
    user_response = test_client.post("/users/", headers=headers, json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]
    
    # Now create a student profile for the user
    student_data = {
        "user_id": user_id,
        "enrollment_date": "2025-01-15",
        "grade_level": 9,
        "parent_name": "Parent Name",
        "parent_email": "parent@example.com"
    }
    
    response = test_client.post("/students/", headers=headers, json=student_data)
    assert response.status_code == 201
    
    student = response.json()
    assert student["user_id"] == user_id
    assert student["grade_level"] == 9

def test_update_student(test_client, admin_user):
    """Test updating a student record"""
    headers = get_auth_header(test_client)
    
    # First create a student
    test_create_student(test_client, admin_user)
    
    # Get the student id
    response = test_client.get("/students/", headers=headers)
    students = response.json()
    student_id = students[0]["id"]
    
    # Update the student
    update_data = {
        "grade_level": 10,
        "parent_name": "Updated Parent Name"
    }
    
    response = test_client.patch(f"/students/{student_id}", headers=headers, json=update_data)
    assert response.status_code == 200
    
    updated_student = response.json()
    assert updated_student["grade_level"] == 10
    assert updated_student["parent_name"] == "Updated Parent Name"

def test_delete_student(test_client, admin_user):
    """Test deleting a student record"""
    headers = get_auth_header(test_client)
    
    # Create a student for the test
    test_create_student(test_client, admin_user)
    
    # Get the student id
    response = test_client.get("/students/", headers=headers)
    students = response.json()
    student_id = students[0]["id"]
    
    # Delete the student
    response = test_client.delete(f"/students/{student_id}", headers=headers)
    assert response.status_code == 204
    
    # Verify the student is deleted
    response = test_client.get(f"/students/{student_id}", headers=headers)
    assert response.status_code == 404