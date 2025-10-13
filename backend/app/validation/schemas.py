import pandera as pa
from pandera import Column, DataFrameSchema, Check
from typing import Optional


# UNHCR Displacement Data Schema
displacement_schema = DataFrameSchema(
    {
        "year": Column(int, Check.in_range(1950, 2100), nullable=False),
        "country_of_origin_iso": Column(str, Check.str_length(3, 3), nullable=True),
        "country_of_asylum_iso": Column(str, Check.str_length(3, 3), nullable=True),
        "refugees": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
        "asylum_seekers": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
        "idps": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
        "returnees": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
        "stateless": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
    },
    strict=False,  # Allow additional columns
    coerce=True,  # Coerce types
)


# World Bank Economic Indicators Schema
economic_schema = DataFrameSchema(
    {
        "country_iso": Column(str, Check.str_length(3, 3), nullable=False),
        "indicator_code": Column(str, Check.str_matches(r"^[A-Z0-9._]+$"), nullable=False),
        "year": Column(int, Check.in_range(1960, 2100), nullable=False),
        "value": Column(float, nullable=True),  # Can be null for missing data
    },
    strict=False,
    coerce=True,
)


# ACLED Conflict Events Schema
conflict_schema = DataFrameSchema(
    {
        "event_date": Column(str, Check.str_matches(r"^\d{4}-\d{2}-\d{2}$"), nullable=False),
        "year": Column(int, Check.in_range(1997, 2100), nullable=False),
        "event_type": Column(
            str,
            Check.isin([
                "Battles",
                "Explosions/Remote violence",
                "Violence against civilians",
                "Protests",
                "Riots",
                "Strategic developments"
            ]),
            nullable=True
        ),
        "latitude": Column(float, Check.in_range(-90, 90), nullable=True),
        "longitude": Column(float, Check.in_range(-180, 180), nullable=True),
        "fatalities": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
    },
    strict=False,
    coerce=True,
)


# NASA POWER Climate Data Schema
climate_schema = DataFrameSchema(
    {
        "date": Column(str, Check.str_matches(r"^\d{4}-\d{2}-\d{2}$"), nullable=False),
        "year": Column(int, Check.in_range(1981, 2100), nullable=False),
        "month": Column(int, Check.in_range(1, 12), nullable=False),
        "day": Column(int, Check.in_range(1, 31), nullable=False),
        "latitude": Column(float, Check.in_range(-90, 90), nullable=False),
        "longitude": Column(float, Check.in_range(-180, 180), nullable=False),
        "t2m": Column(float, Check.in_range(-100, 100), nullable=True),  # Temperature in Celsius
        "prectotcorr": Column(float, Check.greater_than_or_equal_to(0), nullable=True),  # Precipitation
    },
    strict=False,
    coerce=True,
)


def validate_displacement_data(df):
    """Validate UNHCR displacement data."""
    return displacement_schema.validate(df, lazy=True)


def validate_economic_data(df):
    """Validate World Bank economic data."""
    return economic_schema.validate(df, lazy=True)


def validate_conflict_data(df):
    """Validate ACLED conflict data."""
    return conflict_schema.validate(df, lazy=True)


def validate_climate_data(df):
    """Validate NASA POWER climate data."""
    return climate_schema.validate(df, lazy=True)
