import pytest
from fastapi.testclient import TestClient

def test_login(test_client):
    """Test user login endpoint"""
    # First create a user to test with
    user_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
        "role": "STUDENT"
    }
    
    # Register user
    register_response = test_client.post("/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    # Test login
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    
    response = test_client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    
    # Check if token is returned
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    
def test_failed_login(test_client):
    """Test failed login attempts"""
    # Test with wrong password
    login_data = {
        "username": "testuser@example.com",
        "password": "wrongpassword"
    }
    
    response = test_client.post("/auth/token", data=login_data)
    assert response.status_code == 401
    
    # Test with non-existent user
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password"
    }
    
    response = test_client.post("/auth/token", data=login_data)
    assert response.status_code == 401