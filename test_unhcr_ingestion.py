#!/usr/bin/env python3
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/home/theca/hermes-agent/refugee-crisis-prediction/backend')

async def test_unhcr_connector():
    """Test the UNHCR connector by fetching sample data."""
    try:
        from app.connectors.unhcr import UNHCRConnector
        
        print("Testing UNHCR Connector...")
        
        async with UNHCRConnector() as connector:
            # Try to fetch data for a recent year for a few countries
            # Note: The method expects country_code (singular) and we'll loop over countries
            all_data = []
            for country_code in ["AFG", "SYR", "SOM"]:  # Afghanistan, Syria, Somalia
                result = await connector.fetch_population_data(
                    year=2023,
                    country_code=country_code,
                    limit=10
                )
                all_data.extend(result["data"])
            
            print(f"Successfully fetched {len(all_data)} records")
            if all_data:
                print(f"Data sample: {all_data[0]}")
            print(f"Provenance: {result.get('provenance', 'None')}")
            
            return True
            
    except Exception as e:
        print(f"Error testing UNHCR connector: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_unhcr_connector())
    sys.exit(0 if success else 1)