from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.services.etl_service import ETLService

router = APIRouter(prefix="/api/v1/etl", tags=["ETL"])


class PopulateDimDateRequest(BaseModel):
    start_year: int = 1950
    end_year: int = 2100


class PopulateDimCountryRequest(BaseModel):
    countries: List[dict]  # List of {iso3_code, name, region, subregion}


class TransformRequest(BaseModel):
    ingest_run_id: int


@router.post("/dim-date")
async def populate_dim_date(
    request: PopulateDimDateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Populate dim_date dimension table.
    
    Example:
    ```json
    {
        "start_year": 1950,
        "end_year": 2100
    }
    ```
    """
    try:
        service = ETLService(db)
        count = await service.populate_dim_date(
            start_year=request.start_year,
            end_year=request.end_year
        )
        return {"status": "success", "dates_inserted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dim-country")
async def populate_dim_country(
    request: PopulateDimCountryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Populate dim_country dimension table.
    
    Example:
    ```json
    {
        "countries": [
            {"iso3_code": "AFG", "name": "Afghanistan", "region": "Asia", "subregion": "South Asia"},
            {"iso3_code": "SOM", "name": "Somalia", "region": "Africa", "subregion": "East Africa"}
        ]
    }
    ```
    """
    try:
        service = ETLService(db)
        count = await service.populate_dim_country(countries=request.countries)
        return {"status": "success", "countries_inserted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transform/displacement")
async def transform_displacement(
    request: TransformRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Transform displacement data from staging to fact table.
    
    Example:
    ```json
    {
        "ingest_run_id": 1
    }
    ```
    """
    try:
        service = ETLService(db)
        result = await service.transform_displacement_data(ingest_run_id=request.ingest_run_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_etl_status(db: AsyncSession = Depends(get_db)):
    """Get status of curated layer (dimension and fact table counts)."""
    try:
        service = ETLService(db)
        status = await service.get_transformation_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
