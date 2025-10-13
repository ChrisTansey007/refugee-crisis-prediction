from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.services.ingest_service import IngestService

router = APIRouter(prefix="/api/v1/ingest", tags=["Data Ingestion"])


class UNHCRIngestRequest(BaseModel):
    year: int
    country_codes: Optional[List[str]] = None


class WorldBankIngestRequest(BaseModel):
    country_codes: List[str]
    indicator_codes: Optional[List[str]] = None
    start_year: int = 2015
    end_year: Optional[int] = None


class ACLEDIngestRequest(BaseModel):
    api_key: str
    email: str
    country: str
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    event_types: Optional[List[str]] = None


class NASAPowerIngestRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: str  # YYYYMMDD
    end_date: str  # YYYYMMDD
    parameters: Optional[List[str]] = None


@router.post("/unhcr")
async def ingest_unhcr(
    request: UNHCRIngestRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger UNHCR data ingestion.
    
    Example:
    ```json
    {
        "year": 2023,
        "country_codes": ["AFG", "SYR", "SOM"]
    }
    ```
    """
    try:
        service = IngestService(db)
        result = await service.ingest_unhcr_data(
            year=request.year,
            country_codes=request.country_codes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/worldbank")
async def ingest_worldbank(
    request: WorldBankIngestRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger World Bank data ingestion.
    
    Example:
    ```json
    {
        "country_codes": ["AFG", "SYR", "SOM"],
        "indicator_codes": ["NY.GDP.PCAP.CD", "SI.POV.DDAY"],
        "start_year": 2015,
        "end_year": 2023
    }
    ```
    """
    try:
        service = IngestService(db)
        result = await service.ingest_worldbank_data(
            country_codes=request.country_codes,
            indicator_codes=request.indicator_codes,
            start_year=request.start_year,
            end_year=request.end_year
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/acled")
async def ingest_acled(
    request: ACLEDIngestRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger ACLED conflict data ingestion.
    
    Example:
    ```json
    {
        "api_key": "YOUR_API_KEY",
        "email": "your@email.com",
        "country": "Somalia",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "event_types": ["Battles", "Violence against civilians"]
    }
    ```
    """
    try:
        service = IngestService(db)
        result = await service.ingest_acled_data(
            api_key=request.api_key,
            email=request.email,
            country=request.country,
            start_date=request.start_date,
            end_date=request.end_date,
            event_types=request.event_types
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nasa-power")
async def ingest_nasa_power(
    request: NASAPowerIngestRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger NASA POWER climate data ingestion.
    
    Example:
    ```json
    {
        "latitude": 2.0,
        "longitude": 45.3,
        "start_date": "20230101",
        "end_date": "20231231",
        "parameters": ["T2M", "PRECTOTCORR"]
    }
    ```
    """
    try:
        service = IngestService(db)
        result = await service.ingest_nasa_power_data(
            latitude=request.latitude,
            longitude=request.longitude,
            start_date=request.start_date,
            end_date=request.end_date,
            parameters=request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/runs/{run_id}")
async def get_run_status(
    run_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get status of a specific ingest run."""
    service = IngestService(db)
    result = await service.get_ingest_run_status(run_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result
