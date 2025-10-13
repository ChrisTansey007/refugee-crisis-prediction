import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.curated import (
    FactDisplacement, FactEconomic, FactConflict, FactClimate,
    DimCountry, DimDate
)

logger = logging.getLogger(__name__)


class FeatureEngineering:
    """Feature engineering for migration forecasting models."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def extract_displacement_features(
        self,
        country_iso: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        Extract displacement features for a country over time.
        
        Args:
            country_iso: ISO3 country code
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            DataFrame with displacement features
        """
        logger.info(f"Extracting displacement features for {country_iso}")
        
        # Get country ID
        country_result = await self.db.execute(
            select(DimCountry).where(DimCountry.iso3_code == country_iso)
        )
        country = country_result.scalar_one_or_none()
        
        if not country:
            logger.warning(f"Country not found: {country_iso}")
            return pd.DataFrame()
        
        # Query displacement facts
        query = text("""
            SELECT 
                dd.date,
                dd.year,
                dd.month,
                fd.refugees,
                fd.asylum_seekers,
                fd.idps,
                fd.returnees,
                fd.stateless,
                fd.total_displaced
            FROM fact_displacement fd
            JOIN dim_date dd ON fd.date_id = dd.id
            WHERE fd.origin_country_id = :country_id
                AND dd.date BETWEEN :start_date AND :end_date
            ORDER BY dd.date
        """)
        
        result = await self.db.execute(
            query,
            {"country_id": country.id, "start_date": start_date, "end_date": end_date}
        )
        
        rows = result.fetchall()
        
        if not rows:
            logger.warning(f"No displacement data found for {country_iso}")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=[
            "date", "year", "month", "refugees", "asylum_seekers",
            "idps", "returnees", "stateless", "total_displaced"
        ])
        
        # Add lag features (previous periods)
        for col in ["refugees", "asylum_seekers", "idps", "total_displaced"]:
            df[f"{col}_lag1"] = df[col].shift(1)
            df[f"{col}_lag3"] = df[col].shift(3)
            df[f"{col}_lag12"] = df[col].shift(12)
        
        # Add rolling statistics
        for col in ["refugees", "total_displaced"]:
            df[f"{col}_rolling_mean_3"] = df[col].rolling(window=3).mean()
            df[f"{col}_rolling_std_3"] = df[col].rolling(window=3).std()
            df[f"{col}_rolling_mean_12"] = df[col].rolling(window=12).mean()
        
        # Add growth rates
        df["refugees_growth"] = df["refugees"].pct_change()
        df["total_displaced_growth"] = df["total_displaced"].pct_change()
        
        return df
    
    async def extract_economic_features(
        self,
        country_iso: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """Extract economic indicator features."""
        logger.info(f"Extracting economic features for {country_iso}")
        
        # Get country ID
        country_result = await self.db.execute(
            select(DimCountry).where(DimCountry.iso3_code == country_iso)
        )
        country = country_result.scalar_one_or_none()
        
        if not country:
            return pd.DataFrame()
        
        # Query economic facts
        query = text("""
            SELECT 
                dd.date,
                dd.year,
                fe.indicator_code,
                fe.value
            FROM fact_economic fe
            JOIN dim_date dd ON fe.date_id = dd.id
            WHERE fe.country_id = :country_id
                AND dd.date BETWEEN :start_date AND :end_date
            ORDER BY dd.date, fe.indicator_code
        """)
        
        result = await self.db.execute(
            query,
            {"country_id": country.id, "start_date": start_date, "end_date": end_date}
        )
        
        rows = result.fetchall()
        
        if not rows:
            logger.warning(f"No economic data found for {country_iso}")
            return pd.DataFrame()
        
        # Convert to DataFrame and pivot
        df = pd.DataFrame(rows, columns=["date", "year", "indicator_code", "value"])
        df_pivot = df.pivot(index="date", columns="indicator_code", values="value")
        df_pivot.reset_index(inplace=True)
        
        # Add lag features for key indicators
        for col in df_pivot.columns:
            if col not in ["date", "year"]:
                df_pivot[f"{col}_lag1"] = df_pivot[col].shift(1)
                df_pivot[f"{col}_change"] = df_pivot[col].pct_change()
        
        return df_pivot
    
    async def extract_conflict_features(
        self,
        country_iso: str,
        start_date: str,
        end_date: str,
        aggregation: str = "monthly"
    ) -> pd.DataFrame:
        """Extract conflict event features aggregated by time period."""
        logger.info(f"Extracting conflict features for {country_iso}")
        
        # Get country ID
        country_result = await self.db.execute(
            select(DimCountry).where(DimCountry.iso3_code == country_iso)
        )
        country = country_result.scalar_one_or_none()
        
        if not country:
            return pd.DataFrame()
        
        # Query conflict facts
        query = text("""
            SELECT 
                dd.date,
                dd.year,
                dd.month,
                fc.event_type,
                COUNT(*) as event_count,
                SUM(fc.fatalities) as total_fatalities
            FROM fact_conflict fc
            JOIN dim_date dd ON fc.date_id = dd.id
            WHERE fc.country_id = :country_id
                AND dd.date BETWEEN :start_date AND :end_date
            GROUP BY dd.date, dd.year, dd.month, fc.event_type
            ORDER BY dd.date
        """)
        
        result = await self.db.execute(
            query,
            {"country_id": country.id, "start_date": start_date, "end_date": end_date}
        )
        
        rows = result.fetchall()
        
        if not rows:
            logger.warning(f"No conflict data found for {country_iso}")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=[
            "date", "year", "month", "event_type", "event_count", "total_fatalities"
        ])
        
        # Pivot by event type
        df_events = df.pivot_table(
            index=["date", "year", "month"],
            columns="event_type",
            values="event_count",
            fill_value=0
        ).reset_index()
        
        df_fatalities = df.groupby(["date", "year", "month"])["total_fatalities"].sum().reset_index()
        
        # Merge
        df_merged = pd.merge(df_events, df_fatalities, on=["date", "year", "month"])
        
        # Add lag features
        df_merged["total_fatalities_lag1"] = df_merged["total_fatalities"].shift(1)
        df_merged["total_fatalities_rolling_mean_3"] = df_merged["total_fatalities"].rolling(window=3).mean()
        
        return df_merged
    
    async def extract_climate_features(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        aggregation: str = "monthly"
    ) -> pd.DataFrame:
        """Extract climate features for a location."""
        logger.info(f"Extracting climate features for ({latitude}, {longitude})")
        
        # Query climate facts (nearest location within tolerance)
        query = text("""
            SELECT 
                dd.date,
                dd.year,
                dd.month,
                fc.temperature_avg,
                fc.temperature_min,
                fc.temperature_max,
                fc.precipitation,
                fc.humidity,
                fc.wind_speed
            FROM fact_climate fc
            JOIN dim_date dd ON fc.date_id = dd.id
            WHERE ABS(fc.latitude - :latitude) < 0.5
                AND ABS(fc.longitude - :longitude) < 0.5
                AND dd.date BETWEEN :start_date AND :end_date
            ORDER BY dd.date
        """)
        
        result = await self.db.execute(
            query,
            {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date
            }
        )
        
        rows = result.fetchall()
        
        if not rows:
            logger.warning(f"No climate data found for ({latitude}, {longitude})")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=[
            "date", "year", "month", "temperature_avg", "temperature_min",
            "temperature_max", "precipitation", "humidity", "wind_speed"
        ])
        
        # Aggregate to monthly if needed
        if aggregation == "monthly":
            df = df.groupby(["year", "month"]).agg({
                "temperature_avg": "mean",
                "temperature_min": "min",
                "temperature_max": "max",
                "precipitation": "sum",
                "humidity": "mean",
                "wind_speed": "mean"
            }).reset_index()
        
        # Add anomaly features (deviation from mean)
        for col in ["temperature_avg", "precipitation"]:
            df[f"{col}_anomaly"] = df[col] - df[col].mean()
        
        return df
    
    async def create_ml_dataset(
        self,
        country_iso: str,
        start_date: str,
        end_date: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Create complete ML dataset by merging all feature sources.
        
        Args:
            country_iso: ISO3 country code
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            latitude: Latitude for climate data (optional)
            longitude: Longitude for climate data (optional)
        
        Returns:
            DataFrame with all features merged
        """
        logger.info(f"Creating ML dataset for {country_iso}")
        
        # Extract all feature sets
        displacement_df = await self.extract_displacement_features(country_iso, start_date, end_date)
        economic_df = await self.extract_economic_features(country_iso, start_date, end_date)
        conflict_df = await self.extract_conflict_features(country_iso, start_date, end_date)
        
        # Start with displacement as base
        if displacement_df.empty:
            logger.error("No displacement data available")
            return pd.DataFrame()
        
        dataset = displacement_df.copy()
        
        # Merge economic features
        if not economic_df.empty:
            dataset = pd.merge(dataset, economic_df, on="date", how="left")
        
        # Merge conflict features
        if not conflict_df.empty:
            dataset = pd.merge(dataset, conflict_df, on=["date", "year", "month"], how="left")
        
        # Merge climate features if coordinates provided
        if latitude is not None and longitude is not None:
            climate_df = await self.extract_climate_features(latitude, longitude, start_date, end_date)
            if not climate_df.empty:
                dataset = pd.merge(dataset, climate_df, on=["year", "month"], how="left")
        
        # Fill missing values
        dataset.fillna(method="ffill", inplace=True)
        dataset.fillna(0, inplace=True)
        
        logger.info(f"Created dataset with {len(dataset)} rows and {len(dataset.columns)} features")
        return dataset
