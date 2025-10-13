from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import httpx
import logging

logger = logging.getLogger(__name__)


class BaseConnector(ABC):
    """Base class for all data source connectors."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, rate_limit: int = 10):
        self.base_url = base_url
        self.api_key = api_key
        self.rate_limit = rate_limit  # requests per minute
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    @abstractmethod
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Fetch data from the source. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def transform_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw data to standardized format."""
        pass
    
    async def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request with error handling and retries."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if headers is None:
            headers = {}
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching {url}: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error fetching {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            raise
    
    def get_provenance(self, source_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate provenance metadata for data ingestion."""
        return {
            "source": source_name,
            "timestamp": datetime.utcnow().isoformat(),
            "params": params,
            "base_url": self.base_url
        }
