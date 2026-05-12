"""Validation service for orchestrating data validation."""
import pandas as pd
from typing import Dict, Any, Optional
import logging
from .validation.unhcr_validator import UNHCRValidator
from .validation.worldbank_validator import WorldBankValidator
from .validation.acled_validator import ACLEDValidator
from .validation.nasapower_validator import NASAPOWERValidator

logger = logging.getLogger(__name__)


class ValidationService:
    """Service for validating data from various sources."""

    def __init__(self):
        self.validators = {
            "UNHCR": UNHCRValidator(),
            "WorldBank": WorldBankValidator(),
            "ACLED": ACLEDValidator(),
            "NASAPOWER": NASAPOWERValidator()
        }
        logger.info("ValidationService initialized with validators for: %s", list(self.validators.keys()))

    def validate_data(self, source: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate data from a specific source.

        Args:
            source: The data source identifier (UNHCR, WorldBank, ACLED, NASAPOWER)
            data: The data to validate as a pandas DataFrame

        Returns:
            Validation report dictionary
        """
        if source not in self.validators:
            error_msg = f"No validator found for source: {source}"
            logger.error(error_msg)
            return {
                "source": source,
                "record_count": len(data) if data is not None else 0,
                "validation_passed": False,
                "errors": [error_msg],
                "completeness_score": 0.0,
                "consistency_score": 0.0,
                "plausibility_score": 0.0
            }

        validator = self.validators[source]
        logger.info(f"Validating {source} data with {len(data)} records")
        
        try:
            validation_result = validator.validate(data)
            logger.info(f"Validation completed for {source}. Passed: {validation_result.get('validation_passed', False)}")
            return validation_result
        except Exception as e:
            logger.error(f"Error validating {source} data: {e}")
            return {
                "source": source,
                "record_count": len(data) if data is not None else 0,
                "validation_passed": False,
                "errors": [f"Validation error: {str(e)}"],
                "completeness_score": 0.0,
                "consistency_score": 0.0,
                "plausibility_score": 0.0
            }

    def validate_all_sources(self, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
        """Validate data from all sources.

        Args:
            data_dict: Dictionary mapping source names to DataFrames

        Returns:
            Dictionary mapping source names to validation reports
        """
        results = {}
        for source, data in data_dict.items():
            results[source] = self.validate_data(source, data)
        return results

    def get_available_sources(self) -> list:
        """Get list of available data sources for validation."""
        return list(self.validators.keys())
