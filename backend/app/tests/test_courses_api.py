import pytest
from fastapi.testclient import TestClient

def get_auth_header(test_client, email="admin@test.com", password="testpassword"):
    """Helper function to get authentication header"""
    login_data = {
        "username": email,
        "password": password
    }
    
    response = test_client.post("/auth/token", data=login_data)
    data = response.json()
    return {"Authorization": f"Bearer {data['access_token']}"}

def test_get_courses(test_client, admin_user):
    """Test retrieving courses list"""
    headers = get_auth_header(test_client)
    response = test_client.get("/courses/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_course(test_client, admin_user, teacher_user):
    """Test creating a new course"""
    headers = get_auth_header(test_client)
    
    # Create a course
    course_data = {
        "title": "Mathematics 101",
        "description": "Introduction to Algebra",
        "teacher_id": teacher_user.id,
        "credits": 4,
        "semester": "FALL",
        "year": 2025,
        "max_students": 30
    }
    
    response = test_client.post("/courses/", headers=headers, json=course_data)
    assert response.status_code == 201
    
    course = response.json()
    assert course["title"] == "Mathematics 101"
    assert course["credits"] == 4
    assert course["teacher_id"] == teacher_user.id

def test_get_course_by_id(test_client, admin_user, teacher_user):
    """Test retrieving a specific course"""
    headers = get_auth_header(test_client)
    
    # Create a course first
    test_create_course(test_client, admin_user, teacher_user)
    
    # Get all courses
    response = test_client.get("/courses/", headers=headers)
    courses = response.json()
    course_id = courses[0]["id"]
    
    # Get the specific course
    response = test_client.get(f"/courses/{course_id}", headers=headers)
    assert response.status_code == 200
    
    course = response.json()
    assert course["id"] == course_id
    assert course["title"] == "Mathematics 101"

def test_update_course(test_client, admin_user, teacher_user):
    """Test updating a course"""
    headers = get_auth_header(test_client)
    
    # Create a course first
    test_create_course(test_client, admin_user, teacher_user)
    
    # Get the course id
    response = test_client.get("/courses/", headers=headers)
    courses = response.json()
    course_id = courses[0]["id"]
    
    # Update the course
    update_data = {
        "title": "Advanced Mathematics",
        "max_students": 25
    }
    
    response = test_client.patch(f"/courses/{course_id}", headers=headers, json=update_data)
    assert response.status_code == 200
    
    updated_course = response.json()
    assert updated_course["title"] == "Advanced Mathematics"
    assert updated_course["max_students"] == 25
    assert updated_course["credits"] == 4  # Original value should remain

def test_delete_course(test_client, admin_user, teacher_user):
    """Test deleting a course"""
    headers = get_auth_header(test_client)
    
    # Create a course first
    test_create_course(test_client, admin_user, teacher_user)
    
    # Get the course id
    response = test_client.get("/courses/", headers=headers)
    courses = response.json()
    course_id = courses[0]["id"]
    
    # Delete the course
    response = test_client.delete(f"/courses/{course_id}", headers=headers)
    assert response.status_code == 204
    
    # Verify the course is deleted
    response = test_client.get(f"/courses/{course_id}", headers=headers)
    assert response.status_code == 404