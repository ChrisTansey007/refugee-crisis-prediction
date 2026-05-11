#!/usr/bin/env python3
"""
Implementation script for TASK-0003-ingest-world-bank-data
Ingests World Bank economic indicators using the existing IngestService
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, '/home/theca/hermes-agent/refugee-crisis-prediction/backend')

async def ingest_worldbank_data():
    """Ingest World Bank data for key migration indicators."""
    try:
        from app.services.ingest_service import IngestService
        from app.core.database import async_session
        
        print("Starting World Bank data ingestion...")
        print(f"Current time: {datetime.utcnow()}")
        
        # Create a database session
        async with async_session() as db:
            service = IngestService(db)
            
            # Ingest World Bank data for key countries and indicators
            # Focus on major refugee-origin and host countries
            country_codes = ["AFG", "SYR", "VEN", "SSD", "SOM", "COD", "MYA", "UKR"]  # Major refugee origins
            
            print(f"Ingesting World Bank data for {len(country_codes)} countries")
            print(f"Countries: {', '.join(country_codes)}")
            
            # Ingest data for the last 5 years
            end_year = datetime.utcnow().year - 1
            start_year = end_year - 4  # 5 years of data
            print(f"Year range: {start_year} to {end_year}")
            
            # Run the ingestion
            result = await service.ingest_worldbank_data(
                country_codes=country_codes,
                start_year=start_year,
                end_year=end_year
                # indicator_codes=None means use default migration indicators
            )
            
            print()  # Print blank line
            print("Ingestion completed successfully!")
            print(f"Run ID: {result['run_id']}")
            print(f"Status: {result['status']}")
            print(f"Records inserted: {result['records_inserted']}")
            print(f"Records failed: {result.get('records_failed', 0)}")
            print(f"Checksum: {result['checksum']}")
            
            return True
            
    except Exception as e:
        print(f"Error during World Bank ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(ingest_worldbank_data())
    sys.exit(0 if success else 1)
