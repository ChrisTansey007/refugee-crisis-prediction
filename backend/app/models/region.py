from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from app.models.base import Base

class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)  # e.g., "AFG"
    geometry: Mapped[Geometry] = mapped_column(Geometry('MULTIPOLYGON', srid=4326), nullable=True)
