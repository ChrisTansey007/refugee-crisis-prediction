import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.region import Region
from app.models.audit import AuditLog

@pytest.mark.asyncio
async def test_user_model(db_session: AsyncSession):
    """Test User model creation."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active == True

@pytest.mark.asyncio
async def test_region_model(db_session: AsyncSession):
    """Test Region model creation."""
    region = Region(
        name="Test Region",
        code="TST"
    )
    db_session.add(region)
    await db_session.commit()
    await db_session.refresh(region)
    
    assert region.id is not None
    assert region.name == "Test Region"
    assert region.code == "TST"

@pytest.mark.asyncio
async def test_audit_log_model(db_session: AsyncSession):
    """Test AuditLog model creation."""
    # Create user first
    user = User(email="audit@example.com", hashed_password="hash")
    db_session.add(user)
    await db_session.commit()
    
    audit = AuditLog(
        user_id=user.id,
        action="CREATE",
        resource="user",
        resource_id=user.id,
        details="Created test user"
    )
    db_session.add(audit)
    await db_session.commit()
    await db_session.refresh(audit)
    
    assert audit.id is not None
    assert audit.action == "CREATE"
    assert audit.user_id == user.id
