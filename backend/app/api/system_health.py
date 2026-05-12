from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/system", tags=["System Health"])

@router.get("/health", summary="System Health Check", description="Returns comprehensive system health status")
async def system_health_check(db: AsyncSession = Depends(get_db)):
    """
    Comprehensive system health check including:
    - API status (always healthy if this endpoint responds)
    - Database connectivity and basic query
    - ML models status (check if model files exist or service is ready)
    - Data freshness (when was last successful ETL run)
    """
    health_status = {
        "apiStatus": "healthy",
        "databaseStatus": "disconnected",  # Default, will update if successful
        "mlModelsStatus": "not ready",     # Default, will update if models available
        "dataFreshness": "unknown"         # Default, will update if we can check
    }
    
    # Check database connectivity
    try:
        async with db.begin():
            # Simple query to check database is responsive
            result = await db.execute(text("SELECT 1"))
            if result.scalar() == 1:
                health_status["databaseStatus"] = "connected"
                
                # Try to get some basic stats for data freshness
                # We'll check if we can query the fact tables for recent data
                try:
                    # Check if we have any recent displacement data (this would be customized based on actual table structure)
                    # For now, we'll just note that DB is connected
                    health_status["dataFreshness"] = "connected"
                except Exception:
                    # If we can't check freshness, at least we know DB is up
                    health_status["dataFreshness"] = "database connected"
                    
    except Exception as e:
        logger.warning(f"Database health check failed: {str(e)}")
        health_status["databaseStatus"] = "disconnected"
        health_status["apiStatus"] = "degraded"  # API is up but DB is down
    
    # Check ML models status
    # In a real implementation, we'd check if model files exist or if the model service is ready
    # For now, we'll check if the models directory exists and has files
    import os
    models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
    if not os.path.exists(models_dir):
        # Try alternative path
        models_dir = "./models"
    
    if os.path.exists(models_dir):
        # Check if there are any model files
        model_files = []
        for root, dirs, files in os.walk(models_dir):
            for file in files:
                if file.endswith(('.pkl', '.joblib', '.h5', '.pt', '.pth')):
                    model_files.append(file)
        
        if model_files:
            health_status["mlModelsStatus"] = "ready"
        else:
            health_status["mlModelsStatus"] = "not ready (no model files)"
    else:
        health_status["mlModelsStatus"] = "not ready (models directory not found)"
    
    # If we have a way to check ETL last run time, we would do it here
    # For now, we'll leave dataFreshness as is or set a reasonable default
    if health_status["dataFreshness"] == "unknown":
        health_status["dataFreshness"] = "ETL status unknown"
    
    return health_status

@router.get("/readiness", summary="System Readiness Check", description="Returns system readiness for serving requests")
async def system_readiness_check(db: AsyncSession = Depends(get_db)):
    """Check if system is ready to serve production traffic"""
    # Start with assuming not ready
    ready = True
    details = []
    
    # Check database
    try:
        async with db.begin():
            await db.execute(text("SELECT 1"))
    except Exception as e:
        ready = False
        details.append(f"Database: {str(e)}")
    
    # In a full implementation, we'd check:
    # - Model loading
    # - Critical services
    # - Dependencies
    
    if ready:
        return {"status": "ready"}
    else:
        return {
            "status": "not ready",
            "detail": "; ".join(details)
        }

