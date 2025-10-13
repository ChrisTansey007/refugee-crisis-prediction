from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class DataIngestRun(Base):
    """Track data ingestion runs for provenance and auditing."""
    
    __tablename__ = "data_ingest_runs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "UNHCR", "WorldBank"
    run_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "full", "incremental"
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # "running", "success", "failed"
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    records_fetched: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_inserted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_updated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    params: Mapped[dict] = mapped_column(JSON, nullable=True)  # Query parameters used
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    checksum: Mapped[str] = mapped_column(String(64), nullable=True)  # SHA256 of fetched data


class StagingDisplacement(Base):
    """Staging table for raw displacement data from UNHCR."""
    
    __tablename__ = "stg_displacement"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ingest_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    country_of_origin: Mapped[str] = mapped_column(String(255), nullable=True)
    country_of_origin_iso: Mapped[str] = mapped_column(String(3), nullable=True)
    country_of_asylum: Mapped[str] = mapped_column(String(255), nullable=True)
    country_of_asylum_iso: Mapped[str] = mapped_column(String(3), nullable=True)
    refugees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    asylum_seekers: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    idps: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    returnees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stateless: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=True)  # Store original response
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class StagingEconomic(Base):
    """Staging table for economic indicators from World Bank."""
    
    __tablename__ = "stg_economic"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ingest_run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    country_iso: Mapped[str] = mapped_column(String(3), nullable=False)
    country_name: Mapped[str] = mapped_column(String(255), nullable=True)
    indicator_code: Mapped[str] = mapped_column(String(50), nullable=False)
    indicator_name: Mapped[str] = mapped_column(String(255), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[float] = mapped_column(nullable=True)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
