from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from app.connectors.base import BaseConnector

logger = logging.getLogger(__name__)


class ACLEDConnector(BaseConnector):
    """Connector for ACLED (Armed Conflict Location & Event Data Project) API."""
    
    def __init__(self, api_key: str, email: str):
        """
        Initialize ACLED connector.
        
        Args:
            api_key: ACLED API key (register at https://developer.acleddata.com/)
            email: Email associated with ACLED account
        """
        super().__init__(
            base_url="https://api.acleddata.com/acled",
            api_key=api_key,
            rate_limit=10  # 10 requests per minute
        )
        self.email = email
    
    async def fetch_conflict_events(
        self,
        country: str,
        start_date: str,
        end_date: str,
        event_types: Optional[List[str]] = None,
        limit: int = 5000
    ) -> Dict[str, Any]:
        """
        Fetch conflict events from ACLED API.
        
        Args:
            country: Country name (e.g., "Somalia", "Afghanistan")
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            event_types: List of event types to filter (optional)
            limit: Maximum number of records to fetch
        
        Returns:
            Dict containing conflict events and metadata
        """
        params = {
            "key": self.api_key,
            "email": self.email,
            "country": country,
            "event_date": f"{start_date}|{end_date}",
            "event_date_where": "BETWEEN",
            "limit": limit
        }
        
        if event_types:
            params["event_type"] = "|".join(event_types)
        
        try:
            logger.info(f"Fetching ACLED data for {country} ({start_date} to {end_date})")
            raw_data = await self.get("read", params=params)
            transformed = self.transform_data(raw_data)
            
            return {
                "data": transformed,
                "provenance": self.get_provenance("ACLED", {
                    "country": country,
                    "date_range": f"{start_date} to {end_date}",
                    "event_types": event_types
                }),
                "record_count": len(transformed) if isinstance(transformed, list) else 0
            }
        except Exception as e:
            logger.error(f"Failed to fetch ACLED data: {e}")
            raise
    
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Main fetch method (implements abstract method)."""
        country = kwargs.get("country", "Somalia")
        start_date = kwargs.get("start_date", "2023-01-01")
        end_date = kwargs.get("end_date", "2023-12-31")
        event_types = kwargs.get("event_types")
        
        return await self.fetch_conflict_events(
            country=country,
            start_date=start_date,
            end_date=end_date,
            event_types=event_types
        )
    
    def transform_data(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Transform ACLED API response to standardized format.
        
        Expected raw format:
        {
            "success": true,
            "count": 150,
            "data": [
                {
                    "event_id_cnty": "SOM12345",
                    "event_date": "2023-06-15",
                    "year": 2023,
                    "event_type": "Battles",
                    "sub_event_type": "Armed clash",
                    "actor1": "Government Forces",
                    "actor2": "Al-Shabaab",
                    "country": "Somalia",
                    "iso": 706,
                    "region": "Eastern Africa",
                    "latitude": 2.0469,
                    "longitude": 45.3182,
                    "location": "Mogadishu",
                    "fatalities": 5,
                    "notes": "Event description...",
                    ...
                }
            ]
        }
        """
        if not raw_data or "data" not in raw_data:
            logger.warning("No data found in ACLED response")
            return []
        
        data_array = raw_data.get("data", [])
        
        if not data_array:
            logger.warning("Empty data array in ACLED response")
            return []
        
        transformed = []
        for item in data_array:
            transformed_item = {
                "event_id": item.get("event_id_cnty"),
                "event_date": item.get("event_date"),
                "year": item.get("year"),
                "event_type": item.get("event_type"),
                "sub_event_type": item.get("sub_event_type"),
                "actor1": item.get("actor1"),
                "actor2": item.get("actor2"),
                "country": item.get("country"),
                "iso": item.get("iso"),
                "region": item.get("region"),
                "latitude": float(item.get("latitude")) if item.get("latitude") else None,
                "longitude": float(item.get("longitude")) if item.get("longitude") else None,
                "location": item.get("location"),
                "fatalities": int(item.get("fatalities", 0)),
                "notes": item.get("notes"),
                "source": "ACLED",
                "ingested_at": datetime.utcnow().isoformat()
            }
            transformed.append(transformed_item)
        
        logger.info(f"Transformed {len(transformed)} ACLED records")
        return transformed


# ACLED event types
EVENT_TYPES = [
    "Battles",
    "Explosions/Remote violence",
    "Violence against civilians",
    "Protests",
    "Riots",
    "Strategic developments"
]
