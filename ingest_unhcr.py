#!/usr/bin/env python3
"""
Implementation script for TASK-0002-ingest-unhcr-data
Ingests UNHCR refugee data using the existing IngestService
"""
import asyncio
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, '/home/theca/hermes-agent/refugee-crisis-prediction/backend')

async def ingest_unhcr_data():
    """Ingest UNHCR data for the current year."""
    try:
        from app.services.ingest_service import IngestService
        from app.core.database import async_session
        
        print("Starting UNHCR data ingestion...")
        print(f"Current time: {datetime.utcnow()}")
        
        # Create a database session
        async with async_session() as db:
            service = IngestService(db)
            
            # Ingest UNHCR data for the previous year (current year might not be complete)
            year = datetime.utcnow().year - 1
            print(f"Ingesting UNHCR data for year: {year}")
            
            # Ingest data for all countries (no country_codes specified = all countries)
            result = await service.ingest_unhcr_data(
                year=year,
                country_codes=None  # None means all countries
            )
            
            print(f"Ingestion completed successfully!")
            print(f"Run ID: {result['run_id']}")
            print(f"Status: {result['status']}")
            print(f"Records inserted: {result['records_inserted']}")
            print(f"Checksum: {result['checksum']}")
            
            return True
            
    except Exception as e:
        print(f"Error during UNHCR ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(ingest_unhcr_data())
    sys.exit(0 if success else 1)