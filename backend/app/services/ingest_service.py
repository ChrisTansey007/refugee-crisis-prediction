from typing import Dict, Any, List
from datetime import datetime
import hashlib
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.data_ingest import DataIngestRun, StagingDisplacement, StagingEconomic
from app.models.staging_tables import StagingConflict, StagingClimate
from app.connectors.unhcr import UNHCRConnector
from app.connectors.worldbank import WorldBankConnector, MIGRATION_INDICATORS
from app.connectors.acled import ACLEDConnector
from app.connectors.nasa_power import NASAPowerConnector

from app.services.validation_service import ValidationService

logger = logging.getLogger(__name__)


class IngestService:
    """Service for orchestrating data ingestion from external sources."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.validator = ValidationService()
    
    async def ingest_unhcr_data(
        self,
        year: int,
        country_codes: List[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest UNHCR refugee data for specified year and countries.
        
        Args:
            year: Year to fetch data for
            country_codes: List of ISO3 country codes (None = all countries)
        
        Returns:
            Dict with ingestion summary
        """
        # Create ingest run record
        run = DataIngestRun(
            source="UNHCR",
            run_type="full" if not country_codes else "incremental",
            status="running",
            params={"year": year, "country_codes": country_codes}
        )
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        
        try:
            async with UNHCRConnector() as connector:
                if country_codes:
                    all_data = []
                    for country_code in country_codes:
                        result = await connector.fetch_population_data(year=year, country_code=country_code)
                        all_data.extend(result["data"])
                else:
                    result = await connector.fetch_population_data(year=year)
                    all_data = result["data"]
                
                # Calculate checksum
                data_str = json.dumps(all_data, sort_keys=True)
                checksum = hashlib.sha256(data_str.encode()).hexdigest()
                
                # Insert into staging table
                records_inserted = 0
                for record in all_data:
                    staging_record = StagingDisplacement(
                        ingest_run_id=run.id,
                        year=record["year"],
                        country_of_origin=record["country_of_origin"],
                        country_of_origin_iso=record["country_of_origin_iso"],
                        country_of_asylum=record["country_of_asylum"],
                        country_of_asylum_iso=record["country_of_asylum_iso"],
                        refugees=record["refugees"],
                        asylum_seekers=record["asylum_seekers"],
                        idps=record["idps"],
                        returnees=record["returnees"],
                        stateless=record["stateless"],
                        raw_data=record
                    )
                    self.db.add(staging_record)
                    records_inserted += 1
                
                # Update run record
                run.status = "success"
                run.completed_at = datetime.utcnow()
                run.records_fetched = len(all_data)
                run.records_inserted = records_inserted
                run.checksum = checksum
                
                await self.db.commit()
                
                logger.info(f"UNHCR ingestion completed: {records_inserted} records")
                return {
                    "run_id": run.id,
                    "status": "success",
                    "records_inserted": records_inserted,
                    "checksum": checksum
                }
        
        except Exception as e:
            logger.error(f"UNHCR ingestion failed: {e}")
            run.status = "failed"
            run.completed_at = datetime.utcnow()
            run.error_message = str(e)
            await self.db.commit()
            raise
    
    async def ingest_worldbank_data(
        self,
        country_codes: List[str],
        indicator_codes: List[str] = None,
        start_year: int = 2015,
        end_year: int = None
    ) -> Dict[str, Any]:
        """
        Ingest World Bank economic indicators.
        
        Args:
            country_codes: List of ISO3 country codes
            indicator_codes: List of indicator codes (None = use defaults)
            start_year: Start year for data range
            end_year: End year for data range (None = current year - 1)
        
        Returns:
            Dict with ingestion summary
        """
        if end_year is None:
            end_year = datetime.now().year - 1
        
        if indicator_codes is None:
            indicator_codes = list(MIGRATION_INDICATORS.keys())
        
        # Create ingest run record
        run = DataIngestRun(
            source="WorldBank",
            run_type="full",
            status="running",
            params={
                "country_codes": country_codes,
                "indicator_codes": indicator_codes,
                "start_year": start_year,
                "end_year": end_year
            }
        )
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        
        try:
            async with WorldBankConnector() as connector:
                all_data = []
                
                for country_code in country_codes:
                    for indicator_code in indicator_codes:
                        try:
                            result = await connector.fetch_indicator(
                                country_code=country_code,
                                indicator_code=indicator_code,
                                start_year=start_year,
                                end_year=end_year
                            )
                            all_data.extend(result["data"])
                        except Exception as e:
                            logger.warning(f"Failed to fetch {indicator_code} for {country_code}: {e}")
                            run.records_failed += 1
                
                # Calculate checksum
                data_str = json.dumps(all_data, sort_keys=True)
                checksum = hashlib.sha256(data_str.encode()).hexdigest()
                
                # Insert into staging table
                records_inserted = 0
                for record in all_data:
                    staging_record = StagingEconomic(
                        ingest_run_id=run.id,
                        country_iso=record["country_iso"],
                        country_name=record["country_name"],
                        indicator_code=record["indicator_code"],
                        indicator_name=record["indicator_name"],
                        year=record["year"],
                        value=record["value"],
                        unit=record["unit"],
                        raw_data=record
                    )
                    self.db.add(staging_record)
                    records_inserted += 1
                
                # Update run record
                run.status = "success"
                run.completed_at = datetime.utcnow()
                run.records_fetched = len(all_data)
                run.records_inserted = records_inserted
                run.checksum = checksum
                
                await self.db.commit()
                
                logger.info(f"World Bank ingestion completed: {records_inserted} records")
                return {
                    "run_id": run.id,
                    "status": "success",
                    "records_inserted": records_inserted,
                    "records_failed": run.records_failed,
                    "checksum": checksum
                }
        
        except Exception as e:
            logger.error(f"World Bank ingestion failed: {e}")
            run.status = "failed"
            run.completed_at = datetime.utcnow()
            run.error_message = str(e)
            await self.db.commit()
            raise
    
    async def ingest_acled_data(
        self,
        api_key: str,
        email: str,
        country: str,
        start_date: str,
        end_date: str,
        event_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest ACLED conflict data.
        
        Args:
            api_key: ACLED API key
            email: Email associated with ACLED account
            country: Country name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            event_types: List of event types to filter
        
        Returns:
            Dict with ingestion summary
        """
        run = DataIngestRun(
            source="ACLED",
            run_type="full",
            status="running",
            params={
                "country": country,
                "start_date": start_date,
                "end_date": end_date,
                "event_types": event_types
            }
        )
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        
        try:
            async with ACLEDConnector(api_key=api_key, email=email) as connector:
                result = await connector.fetch_conflict_events(
                    country=country,
                    start_date=start_date,
                    end_date=end_date,
                    event_types=event_types
                )
                
                all_data = result["data"]
                
                # Calculate checksum
                data_str = json.dumps(all_data, sort_keys=True)
                checksum = hashlib.sha256(data_str.encode()).hexdigest()
                
                # Insert into staging table
                records_inserted = 0
                for record in all_data:
                    staging_record = StagingConflict(
                        ingest_run_id=run.id,
                        event_id=record["event_id"],
                        event_date=record["event_date"],
                        year=record["year"],
                        event_type=record["event_type"],
                        sub_event_type=record["sub_event_type"],
                        actor1=record["actor1"],
                        actor2=record["actor2"],
                        country=record["country"],
                        iso=record["iso"],
                        region=record["region"],
                        latitude=record["latitude"],
                        longitude=record["longitude"],
                        location=record["location"],
                        fatalities=record["fatalities"],
                        notes=record["notes"],
                        raw_data=record
                    )
                    self.db.add(staging_record)
                    records_inserted += 1
                
                # Update run record
                run.status = "success"
                run.completed_at = datetime.utcnow()
                run.records_fetched = len(all_data)
                run.records_inserted = records_inserted
                run.checksum = checksum
                
                await self.db.commit()
                
                logger.info(f"ACLED ingestion completed: {records_inserted} records")
                return {
                    "run_id": run.id,
                    "status": "success",
                    "records_inserted": records_inserted,
                    "checksum": checksum
                }
        
        except Exception as e:
            logger.error(f"ACLED ingestion failed: {e}")
            run.status = "failed"
            run.completed_at = datetime.utcnow()
            run.error_message = str(e)
            await self.db.commit()
            raise
    
    async def ingest_nasa_power_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        parameters: List[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest NASA POWER climate data.
        
        Args:
            latitude: Latitude (-90 to 90)
            longitude: Longitude (-180 to 180)
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            parameters: List of climate parameters
        
        Returns:
            Dict with ingestion summary
        """
        run = DataIngestRun(
            source="NASA_POWER",
            run_type="full",
            status="running",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "parameters": parameters
            }
        )
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        
        try:
            async with NASAPowerConnector() as connector:
                result = await connector.fetch_climate_data(
                    latitude=latitude,
                    longitude=longitude,
                    start_date=start_date,
                    end_date=end_date,
                    parameters=parameters
                )
                
                all_data = result["data"]
                
                # Calculate checksum
                data_str = json.dumps(all_data, sort_keys=True)
                checksum = hashlib.sha256(data_str.encode()).hexdigest()
                
                # Insert into staging table
                records_inserted = 0
                for record in all_data:
                    staging_record = StagingClimate(
                        ingest_run_id=run.id,
                        date=record["date"],
                        year=record["year"],
                        month=record["month"],
                        day=record["day"],
                        latitude=record["latitude"],
                        longitude=record["longitude"],
                        t2m=record.get("t2m"),
                        t2m_min=record.get("t2m_min"),
                        t2m_max=record.get("t2m_max"),
                        prectotcorr=record.get("prectotcorr"),
                        rh2m=record.get("rh2m"),
                        ws2m=record.get("ws2m"),
                        allsky_sfc_sw_dwn=record.get("allsky_sfc_sw_dwn"),
                        evptrns=record.get("evptrns"),
                        raw_data=record
                    )
                    self.db.add(staging_record)
                    records_inserted += 1
                
                # Update run record
                run.status = "success"
                run.completed_at = datetime.utcnow()
                run.records_fetched = len(all_data)
                run.records_inserted = records_inserted
                run.checksum = checksum
                
                await self.db.commit()
                
                logger.info(f"NASA POWER ingestion completed: {records_inserted} records")
                return {
                    "run_id": run.id,
                    "status": "success",
                    "records_inserted": records_inserted,
                    "checksum": checksum
                }
        
        except Exception as e:
            logger.error(f"NASA POWER ingestion failed: {e}")
            run.status = "failed"
            run.completed_at = datetime.utcnow()
            run.error_message = str(e)
            await self.db.commit()
            raise
    
    async def get_ingest_run_status(self, run_id: int) -> Dict[str, Any]:
        """Get status of a specific ingest run."""
        result = await self.db.execute(
            select(DataIngestRun).where(DataIngestRun.id == run_id)
        )
        run = result.scalar_one_or_none()
        
        if not run:
            return {"error": "Run not found"}
        
        return {
            "run_id": run.id,
            "source": run.source,
            "status": run.status,
            "started_at": run.started_at.isoformat(),
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
            "records_fetched": run.records_fetched,
            "records_inserted": run.records_inserted,
            "records_failed": run.records_failed,
            "error_message": run.error_message
        }
