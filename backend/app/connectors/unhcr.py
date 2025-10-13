from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from app.connectors.base import BaseConnector

logger = logging.getLogger(__name__)


class UNHCRConnector(BaseConnector):
    """Connector for UNHCR Refugee Statistics API."""
    
    def __init__(self):
        super().__init__(base_url="https://api.unhcr.org/population/v1")
    
    async def fetch_population_data(
        self,
        year: int,
        country_code: Optional[str] = None,
        limit: int = 1000
    ) -> Dict[str, Any]:
        """
        Fetch refugee population data from UNHCR API.
        
        Args:
            year: Year to fetch data for
            country_code: ISO3 country code (optional, fetches all if None)
            limit: Maximum number of records to fetch
        
        Returns:
            Dict containing population data and metadata
        """
        params = {
            "year": year,
            "limit": limit
        }
        
        if country_code:
            params["coo_iso"] = country_code  # Country of origin
        
        try:
            logger.info(f"Fetching UNHCR population data for year {year}")
            raw_data = await self.get("population/", params=params)
            transformed = self.transform_data(raw_data)
            
            return {
                "data": transformed,
                "provenance": self.get_provenance("UNHCR", params),
                "record_count": len(transformed) if isinstance(transformed, list) else 1
            }
        except Exception as e:
            logger.error(f"Failed to fetch UNHCR data: {e}")
            raise
    
    async def fetch_asylum_applications(
        self,
        year: int,
        country_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch asylum application statistics."""
        params = {"year": year}
        if country_code:
            params["coa_iso"] = country_code  # Country of asylum
        
        try:
            logger.info(f"Fetching UNHCR asylum applications for year {year}")
            raw_data = await self.get("asylumApplications/", params=params)
            transformed = self.transform_data(raw_data)
            
            return {
                "data": transformed,
                "provenance": self.get_provenance("UNHCR_Asylum", params),
                "record_count": len(transformed) if isinstance(transformed, list) else 1
            }
        except Exception as e:
            logger.error(f"Failed to fetch UNHCR asylum data: {e}")
            raise
    
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Main fetch method (implements abstract method)."""
        year = kwargs.get("year", datetime.now().year - 1)
        country_code = kwargs.get("country_code")
        
        return await self.fetch_population_data(year=year, country_code=country_code)
    
    def transform_data(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Transform UNHCR API response to standardized format.
        
        Expected raw format:
        {
            "items": [
                {
                    "year": 2023,
                    "coo_name": "Afghanistan",
                    "coo_iso": "AFG",
                    "coa_name": "Pakistan",
                    "coa_iso": "PAK",
                    "refugees": 1500000,
                    "asylum_seekers": 50000,
                    ...
                }
            ]
        }
        """
        if not raw_data or "items" not in raw_data:
            logger.warning("No items found in UNHCR response")
            return []
        
        transformed = []
        for item in raw_data.get("items", []):
            transformed_item = {
                "year": item.get("year"),
                "country_of_origin": item.get("coo_name"),
                "country_of_origin_iso": item.get("coo_iso"),
                "country_of_asylum": item.get("coa_name"),
                "country_of_asylum_iso": item.get("coa_iso"),
                "refugees": item.get("refugees", 0),
                "asylum_seekers": item.get("asylum_seekers", 0),
                "idps": item.get("idps", 0),
                "returnees": item.get("returnees", 0),
                "stateless": item.get("stateless", 0),
                "source": "UNHCR",
                "ingested_at": datetime.utcnow().isoformat()
            }
            transformed.append(transformed_item)
        
        logger.info(f"Transformed {len(transformed)} UNHCR records")
        return transformed
