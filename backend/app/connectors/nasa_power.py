from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from app.connectors.base import BaseConnector

logger = logging.getLogger(__name__)


class NASAPowerConnector(BaseConnector):
    """Connector for NASA POWER (Prediction Of Worldwide Energy Resources) API."""
    
    def __init__(self):
        super().__init__(base_url="https://power.larc.nasa.gov/api/temporal/daily/point")
    
    async def fetch_climate_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        parameters: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Fetch climate data from NASA POWER API for a specific location.
        
        Args:
            latitude: Latitude (-90 to 90)
            longitude: Longitude (-180 to 180)
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            parameters: List of climate parameters (default: T2M, PRECTOTCORR)
        
        Returns:
            Dict containing climate data and metadata
        """
        if parameters is None:
            parameters = ["T2M", "PRECTOTCORR"]  # Temperature, Precipitation
        
        params = {
            "parameters": ",".join(parameters),
            "community": "AG",  # Agricultural community
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }
        
        try:
            logger.info(f"Fetching NASA POWER data for ({latitude}, {longitude})")
            raw_data = await self.get("", params=params)
            transformed = self.transform_data(raw_data, latitude, longitude)
            
            return {
                "data": transformed,
                "provenance": self.get_provenance("NASA_POWER", {
                    "latitude": latitude,
                    "longitude": longitude,
                    "date_range": f"{start_date} to {end_date}",
                    "parameters": parameters
                }),
                "record_count": len(transformed) if isinstance(transformed, list) else 0
            }
        except Exception as e:
            logger.error(f"Failed to fetch NASA POWER data: {e}")
            raise
    
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Main fetch method (implements abstract method)."""
        latitude = kwargs.get("latitude", 2.0)
        longitude = kwargs.get("longitude", 45.3)
        start_date = kwargs.get("start_date", "20230101")
        end_date = kwargs.get("end_date", "20231231")
        parameters = kwargs.get("parameters")
        
        return await self.fetch_climate_data(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            parameters=parameters
        )
    
    def transform_data(self, raw_data: Dict[str, Any], latitude: float, longitude: float) -> List[Dict[str, Any]]:
        """
        Transform NASA POWER API response to standardized format.
        
        Expected raw format:
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [45.3, 2.0]
            },
            "properties": {
                "parameter": {
                    "T2M": {
                        "20230101": 28.5,
                        "20230102": 29.1,
                        ...
                    },
                    "PRECTOTCORR": {
                        "20230101": 0.0,
                        "20230102": 2.5,
                        ...
                    }
                }
            },
            "header": {...}
        }
        """
        if not raw_data or "properties" not in raw_data:
            logger.warning("No properties found in NASA POWER response")
            return []
        
        properties = raw_data.get("properties", {})
        parameter_data = properties.get("parameter", {})
        
        if not parameter_data:
            logger.warning("No parameter data in NASA POWER response")
            return []
        
        # Restructure from parameter-first to date-first format
        transformed = []
        
        # Get all dates from the first parameter
        first_param = list(parameter_data.keys())[0]
        dates = list(parameter_data[first_param].keys())
        
        for date_str in dates:
            # Parse date
            try:
                date_obj = datetime.strptime(date_str, "%Y%m%d")
            except ValueError:
                logger.warning(f"Invalid date format: {date_str}")
                continue
            
            record = {
                "date": date_obj.date().isoformat(),
                "year": date_obj.year,
                "month": date_obj.month,
                "day": date_obj.day,
                "latitude": latitude,
                "longitude": longitude,
                "source": "NASA_POWER",
                "ingested_at": datetime.utcnow().isoformat()
            }
            
            # Add all parameter values for this date
            for param_name, param_values in parameter_data.items():
                value = param_values.get(date_str)
                if value is not None and value != -999:  # -999 is missing data flag
                    record[param_name.lower()] = float(value)
                else:
                    record[param_name.lower()] = None
            
            transformed.append(record)
        
        logger.info(f"Transformed {len(transformed)} NASA POWER records")
        return transformed


# Common NASA POWER parameters for migration forecasting
CLIMATE_PARAMETERS = {
    "T2M": "Temperature at 2 Meters (°C)",
    "T2M_MIN": "Minimum Temperature at 2 Meters (°C)",
    "T2M_MAX": "Maximum Temperature at 2 Meters (°C)",
    "PRECTOTCORR": "Precipitation Corrected (mm/day)",
    "RH2M": "Relative Humidity at 2 Meters (%)",
    "WS2M": "Wind Speed at 2 Meters (m/s)",
    "ALLSKY_SFC_SW_DWN": "All Sky Surface Shortwave Downward Irradiance (kW-hr/m²/day)",
    "EVPTRNS": "Evapotranspiration Energy Flux (MJ/m²/day)"
}
