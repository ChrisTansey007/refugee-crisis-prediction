from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import engine
from app.api import ingest, etl, ml

# Set up logging first
setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="Migration Forecasting System",
    description="AI-powered platform for predicting forced migration patterns",
    version="0.4.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include API routers
app.include_router(ingest.router)
app.include_router(etl.router)
app.include_router(ml.router)

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# Health endpoint
@app.get("/health", summary="Health Check", description="Returns application health status")
async def health_check():
    return {"status": "healthy", "version": "0.4.0"}

# Readiness endpoint
@app.get("/readiness", summary="Readiness Check", description="Returns application readiness status")
async def readiness_check():
    # Check DB connection
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        return {"status": "not ready", "detail": f"Database connection failed: {str(e)}"}
    
    # TODO: Check Redis in Phase 2
    return {"status": "ready"}

# Placeholder for metrics (already exposed at /metrics via Instrumentator)
# No custom metrics in Sprint 1-2

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
