from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.curated import DimCountry, DimDate, FactDisplacement, FactEconomic, FactConflict, FactClimate
from app.models.data_ingest import StagingDisplacement, StagingEconomic
from app.models.staging_tables import StagingConflict, StagingClimate
from app.validation.schemas import (
    validate_displacement_data,
    validate_economic_data,
    validate_conflict_data,
    validate_climate_data
)

logger = logging.getLogger(__name__)


class ETLService:
    """Service for ETL operations: staging → curated layer."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def populate_dim_date(self, start_year: int = 1950, end_year: int = 2100) -> int:
        """
        Populate dim_date with all dates in range.
        
        Args:
            start_year: Start year
            end_year: End year
        
        Returns:
            Number of dates inserted
        """
        logger.info(f"Populating dim_date from {start_year} to {end_year}")
        
        # Check if already populated
        result = await self.db.execute(select(DimDate).limit(1))
        if result.scalar_one_or_none():
            logger.info("dim_date already populated")
            return 0
        
        dates = []
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        current_date = start_date
        
        while current_date <= end_date:
            date_record = DimDate(
                date=current_date.strftime("%Y-%m-%d"),
                year=current_date.year,
                quarter=(current_date.month - 1) // 3 + 1,
                month=current_date.month,
                month_name=current_date.strftime("%B"),
                day=current_date.day,
                day_of_week=current_date.weekday(),
                day_name=current_date.strftime("%A"),
                is_weekend=current_date.weekday() >= 5
            )
            dates.append(date_record)
            current_date += timedelta(days=1)
        
        self.db.add_all(dates)
        await self.db.commit()
        
        logger.info(f"Inserted {len(dates)} dates into dim_date")
        return len(dates)
    
    async def populate_dim_country(self, countries: List[Dict[str, str]]) -> int:
        """
        Populate dim_country with country data.
        
        Args:
            countries: List of dicts with keys: iso3_code, name, region, subregion
        
        Returns:
            Number of countries inserted
        """
        logger.info(f"Populating dim_country with {len(countries)} countries")
        
        inserted = 0
        for country_data in countries:
            # Check if exists
            result = await self.db.execute(
                select(DimCountry).where(DimCountry.iso3_code == country_data["iso3_code"])
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                country = DimCountry(
                    iso3_code=country_data["iso3_code"],
                    name=country_data["name"],
                    region=country_data.get("region"),
                    subregion=country_data.get("subregion")
                )
                self.db.add(country)
                inserted += 1
        
        await self.db.commit()
        logger.info(f"Inserted {inserted} countries into dim_country")
        return inserted
    
    async def transform_displacement_data(self, ingest_run_id: int) -> Dict[str, Any]:
        """
        Transform staging displacement data to fact table.
        
        Args:
            ingest_run_id: ID of the ingest run to transform
        
        Returns:
            Dict with transformation summary
        """
        logger.info(f"Transforming displacement data from run {ingest_run_id}")
        
        # Fetch staging data
        result = await self.db.execute(
            select(StagingDisplacement).where(StagingDisplacement.ingest_run_id == ingest_run_id)
        )
        staging_records = result.scalars().all()
        
        if not staging_records:
            logger.warning(f"No staging records found for run {ingest_run_id}")
            return {"records_transformed": 0, "records_failed": 0}
        
        # Convert to DataFrame for validation
        df = pd.DataFrame([{
            "year": r.year,
            "country_of_origin_iso": r.country_of_origin_iso,
            "country_of_asylum_iso": r.country_of_asylum_iso,
            "refugees": r.refugees,
            "asylum_seekers": r.asylum_seekers,
            "idps": r.idps,
            "returnees": r.returnees,
            "stateless": r.stateless
        } for r in staging_records])
        
        # Validate
        try:
            validated_df = validate_displacement_data(df)
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return {"records_transformed": 0, "records_failed": len(staging_records), "error": str(e)}
        
        # Transform to fact table
        records_transformed = 0
        records_failed = 0
        
        for _, row in validated_df.iterrows():
            try:
                # Get date_id
                date_str = f"{row['year']}-01-01"  # Use Jan 1 for annual data
                date_result = await self.db.execute(
                    select(DimDate).where(DimDate.date == date_str)
                )
                date_record = date_result.scalar_one_or_none()
                
                if not date_record:
                    logger.warning(f"Date not found: {date_str}")
                    records_failed += 1
                    continue
                
                # Get country IDs
                origin_country_id = None
                asylum_country_id = None
                
                if pd.notna(row["country_of_origin_iso"]):
                    origin_result = await self.db.execute(
                        select(DimCountry).where(DimCountry.iso3_code == row["country_of_origin_iso"])
                    )
                    origin_country = origin_result.scalar_one_or_none()
                    origin_country_id = origin_country.id if origin_country else None
                
                if pd.notna(row["country_of_asylum_iso"]):
                    asylum_result = await self.db.execute(
                        select(DimCountry).where(DimCountry.iso3_code == row["country_of_asylum_iso"])
                    )
                    asylum_country = asylum_result.scalar_one_or_none()
                    asylum_country_id = asylum_country.id if asylum_country else None
                
                # Calculate total
                total_displaced = (
                    row["refugees"] + row["asylum_seekers"] + 
                    row["idps"] + row["returnees"] + row["stateless"]
                )
                
                # Insert fact record
                fact = FactDisplacement(
                    date_id=date_record.id,
                    origin_country_id=origin_country_id,
                    asylum_country_id=asylum_country_id,
                    refugees=int(row["refugees"]),
                    asylum_seekers=int(row["asylum_seekers"]),
                    idps=int(row["idps"]),
                    returnees=int(row["returnees"]),
                    stateless=int(row["stateless"]),
                    total_displaced=int(total_displaced),
                    source_run_id=ingest_run_id
                )
                self.db.add(fact)
                records_transformed += 1
            
            except Exception as e:
                logger.error(f"Failed to transform record: {e}")
                records_failed += 1
        
        await self.db.commit()
        
        logger.info(f"Transformed {records_transformed} displacement records, {records_failed} failed")
        return {
            "records_transformed": records_transformed,
            "records_failed": records_failed
        }
    
    async def get_transformation_status(self) -> Dict[str, Any]:
        """Get status of curated layer."""
        from sqlalchemy import func
        
        # Count records in each fact table
        displacement_count = await self.db.scalar(select(func.count()).select_from(FactDisplacement))
        economic_count = await self.db.scalar(select(func.count()).select_from(FactEconomic))
        conflict_count = await self.db.scalar(select(func.count()).select_from(FactConflict))
        climate_count = await self.db.scalar(select(func.count()).select_from(FactClimate))
        
        country_count = await self.db.scalar(select(func.count()).select_from(DimCountry))
        date_count = await self.db.scalar(select(func.count()).select_from(DimDate))
        
        return {
            "dimensions": {
                "countries": country_count or 0,
                "dates": date_count or 0
            },
            "facts": {
                "displacement": displacement_count or 0,
                "economic": economic_count or 0,
                "conflict": conflict_count or 0,
                "climate": climate_count or 0
            }
        }
