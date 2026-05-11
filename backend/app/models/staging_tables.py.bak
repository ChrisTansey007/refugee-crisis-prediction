from datetime import datetime
from sqlalchemy import String, Integer, Float, Text, DateTime, JSON, Date, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class StagingConflict(Base):
    """Staging table for conflict events from ACLED."""
    
    __tablename__ = "stg_conflict"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ingest_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[str] = mapped_column(String(50), nullable=True)
    event_date: Mapped[str] = mapped_column(String(10), nullable=False)  # YYYY-MM-DD
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=True)
    sub_event_type: Mapped[str] = mapped_column(String(100), nullable=True)
    actor1: Mapped[str] = mapped_column(String(255), nullable=True)
    actor2: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    iso: Mapped[int] = mapped_column(Integer, nullable=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    fatalities: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class StagingClimate(Base):
    """Staging table for climate data from NASA POWER."""
    
    __tablename__ = "stg_climate"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ingest_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[str] = mapped_column(String(10), nullable=False)  # YYYY-MM-DD
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    # Climate parameters
    t2m: Mapped[float] = mapped_column(Float, nullable=True)  # Temperature
    t2m_min: Mapped[float] = mapped_column(Float, nullable=True)
    t2m_max: Mapped[float] = mapped_column(Float, nullable=True)
    prectotcorr: Mapped[float] = mapped_column(Float, nullable=True)  # Precipitation
    rh2m: Mapped[float] = mapped_column(Float, nullable=True)  # Humidity
    ws2m: Mapped[float] = mapped_column(Float, nullable=True)  # Wind speed
    allsky_sfc_sw_dwn: Mapped[float] = mapped_column(Float, nullable=True)  # Solar radiation
    evptrns: Mapped[float] = mapped_column(Float, nullable=True)  # Evapotranspiration
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
