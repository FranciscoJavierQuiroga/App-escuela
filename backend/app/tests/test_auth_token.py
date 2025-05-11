import pytest
from datetime import timedelta
from app.auth.token import create_access_token, verify_token

def test_create_access_token():
    """Test token creation"""
    # Test with user_id only
    token = create_access_token(user_id=1)
    assert token is not None
    
    # Test with expiration
    token_with_exp = create_access_token(user_id=1, expires_delta=timedelta(minutes=15))
    assert token_with_exp is not None

def test_verify_token():
    """Test token verification"""
    # Create a token for verification
    token = create_access_token(user_id=1)
    
    # Verify the token
    payload = verify_token(token)
    assert payload is not None
    assert payload.get("sub") == "1"  # sub is string representation of user_id
    
    # Additional tests could include:
    # - Testing expired tokens
    # - Testing invalid tokens