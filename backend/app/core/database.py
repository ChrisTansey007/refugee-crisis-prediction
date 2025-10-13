from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async engine
engine = create_async_engine(settings.database_url, echo=False)

# Create async session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency for FastAPI
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
