from datetime import timedelta
from app.core.jwt import create_access_token, decode_access_token

def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)

def test_decode_access_token():
    """Test JWT token decoding."""
    data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert decoded["sub"] == "test@example.com"
    assert decoded["user_id"] == 1
    assert "exp" in decoded

def test_decode_invalid_token():
    """Test decoding invalid token."""
    invalid_token = "invalid.token.here"
    decoded = decode_access_token(invalid_token)
    
    assert decoded is None
