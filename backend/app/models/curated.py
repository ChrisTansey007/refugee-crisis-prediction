from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from app.models.base import Base


class DimCountry(Base):
    """Dimension table for countries."""
    
    __tablename__ = "dim_country"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    iso3_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    subregion: Mapped[str] = mapped_column(String(255), nullable=True)
    geometry: Mapped[Geometry] = mapped_column(Geometry('MULTIPOLYGON', srid=4326), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class DimDate(Base):
    """Dimension table for dates."""
    
    __tablename__ = "dim_date"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)  # YYYY-MM-DD
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    quarter: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    month_name: Mapped[str] = mapped_column(String(20), nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    day_name: Mapped[str] = mapped_column(String(20), nullable=False)
    is_weekend: Mapped[bool] = mapped_column(nullable=False)


class FactDisplacement(Base):
    """Fact table for displacement data."""
    
    __tablename__ = "fact_displacement"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False)
    origin_country_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_country.id"), nullable=True)
    asylum_country_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_country.id"), nullable=True)
    refugees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    asylum_seekers: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    idps: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    returnees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stateless: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_displaced: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    source_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class FactEconomic(Base):
    """Fact table for economic indicators."""
    
    __tablename__ = "fact_economic"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_country.id"), nullable=False)
    indicator_code: Mapped[str] = mapped_column(String(50), nullable=False)
    indicator_name: Mapped[str] = mapped_column(String(255), nullable=True)
    value: Mapped[float] = mapped_column(Float, nullable=True)
    source_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class FactConflict(Base):
    """Fact table for conflict events."""
    
    __tablename__ = "fact_conflict"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_country.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=True)
    sub_event_type: Mapped[str] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    fatalities: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    source_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class FactClimate(Base):
    """Fact table for climate data."""
    
    __tablename__ = "fact_climate"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_id: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    temperature_avg: Mapped[float] = mapped_column(Float, nullable=True)
    temperature_min: Mapped[float] = mapped_column(Float, nullable=True)
    temperature_max: Mapped[float] = mapped_column(Float, nullable=True)
    precipitation: Mapped[float] = mapped_column(Float, nullable=True)
    humidity: Mapped[float] = mapped_column(Float, nullable=True)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=True)
    source_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


# Create composite indexes for common queries
Index('ix_fact_displacement_date_origin', FactDisplacement.date_id, FactDisplacement.origin_country_id)
Index('ix_fact_economic_date_country', FactEconomic.date_id, FactEconomic.country_id, FactEconomic.indicator_code)
Index('ix_fact_conflict_date_country', FactConflict.date_id, FactConflict.country_id)
Index('ix_fact_climate_date_location', FactClimate.date_id, FactClimate.latitude, FactClimate.longitude)
