from app.core.security import get_password_hash, verify_password

def test_password_hashing():
    """Test password hashing."""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert len(hashed) > 0

def test_password_verification():
    """Test password verification."""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) == True
    assert verify_password("wrong_password", hashed) == False
