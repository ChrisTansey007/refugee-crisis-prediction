from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from app.connectors.base import BaseConnector

logger = logging.getLogger(__name__)


class WorldBankConnector(BaseConnector):
    """Connector for World Bank Indicators API."""
    
    def __init__(self):
        super().__init__(base_url="https://api.worldbank.org/v2")
    
    async def fetch_indicator(
        self,
        country_code: str,
        indicator_code: str,
        start_year: int,
        end_year: int
    ) -> Dict[str, Any]:
        """
        Fetch a specific indicator for a country.
        
        Args:
            country_code: ISO3 country code (e.g., 'SOM' for Somalia)
            indicator_code: World Bank indicator code (e.g., 'NY.GDP.PCAP.CD')
            start_year: Start year for data range
            end_year: End year for data range
        
        Returns:
            Dict containing indicator data and metadata
        """
        endpoint = f"country/{country_code}/indicator/{indicator_code}"
        params = {
            "date": f"{start_year}:{end_year}",
            "format": "json",
            "per_page": 500
        }
        
        try:
            logger.info(f"Fetching World Bank indicator {indicator_code} for {country_code}")
            raw_data = await self.get(endpoint, params=params)
            transformed = self.transform_data(raw_data, indicator_code)
            
            return {
                "data": transformed,
                "provenance": self.get_provenance("WorldBank", {
                    "country": country_code,
                    "indicator": indicator_code,
                    "date_range": f"{start_year}-{end_year}"
                }),
                "record_count": len(transformed) if isinstance(transformed, list) else 0
            }
        except Exception as e:
            logger.error(f"Failed to fetch World Bank data: {e}")
            raise
    
    async def fetch_multiple_indicators(
        self,
        country_code: str,
        indicator_codes: List[str],
        start_year: int,
        end_year: int
    ) -> Dict[str, Any]:
        """Fetch multiple indicators for a country."""
        results = {}
        
        for indicator_code in indicator_codes:
            try:
                result = await self.fetch_indicator(
                    country_code=country_code,
                    indicator_code=indicator_code,
                    start_year=start_year,
                    end_year=end_year
                )
                results[indicator_code] = result
            except Exception as e:
                logger.error(f"Failed to fetch {indicator_code}: {e}")
                results[indicator_code] = {"error": str(e)}
        
        return results
    
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Main fetch method (implements abstract method)."""
        country_code = kwargs.get("country_code", "SOM")
        indicator_code = kwargs.get("indicator_code", "NY.GDP.PCAP.CD")
        start_year = kwargs.get("start_year", 2015)
        end_year = kwargs.get("end_year", datetime.now().year - 1)
        
        return await self.fetch_indicator(
            country_code=country_code,
            indicator_code=indicator_code,
            start_year=start_year,
            end_year=end_year
        )
    
    def transform_data(self, raw_data: Dict[str, Any], indicator_code: str) -> List[Dict[str, Any]]:
        """
        Transform World Bank API response to standardized format.
        
        Expected raw format:
        [
            {
                "page": 1,
                "pages": 1,
                "per_page": 500,
                "total": 9
            },
            [
                {
                    "indicator": {"id": "NY.GDP.PCAP.CD", "value": "GDP per capita"},
                    "country": {"id": "SOM", "value": "Somalia"},
                    "countryiso3code": "SOM",
                    "date": "2023",
                    "value": 450.5,
                    "unit": "",
                    "obs_status": "",
                    "decimal": 1
                },
                ...
            ]
        ]
        """
        if not raw_data or not isinstance(raw_data, list) or len(raw_data) < 2:
            logger.warning("Invalid World Bank response format")
            return []
        
        # World Bank API returns [metadata, data_array]
        data_array = raw_data[1] if len(raw_data) > 1 else []
        
        if not data_array:
            logger.warning(f"No data found for indicator {indicator_code}")
            return []
        
        transformed = []
        for item in data_array:
            if item.get("value") is None:
                continue  # Skip null values
            
            transformed_item = {
                "country_iso": item.get("countryiso3code"),
                "country_name": item.get("country", {}).get("value"),
                "indicator_code": indicator_code,
                "indicator_name": item.get("indicator", {}).get("value"),
                "year": int(item.get("date")),
                "value": float(item.get("value")) if item.get("value") is not None else None,
                "unit": item.get("unit", ""),
                "source": "WorldBank",
                "ingested_at": datetime.utcnow().isoformat()
            }
            transformed.append(transformed_item)
        
        logger.info(f"Transformed {len(transformed)} World Bank records for {indicator_code}")
        return transformed


# Common World Bank indicators for migration forecasting
MIGRATION_INDICATORS = {
    "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
    "SI.POV.DDAY": "Poverty headcount ratio at $2.15/day (2017 PPP)",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "MS.MIL.XPND.GD.ZS": "Military expenditure (% of GDP)",
    "AG.LND.PRCP.MM": "Average precipitation in depth (mm per year)",
    "SP.POP.TOTL": "Population, total",
    "SP.URB.TOTL.IN.ZS": "Urban population (% of total population)",
    "SH.DYN.MORT": "Mortality rate, under-5 (per 1,000 live births)",
    "SE.PRM.ENRR": "School enrollment, primary (% gross)"
}
