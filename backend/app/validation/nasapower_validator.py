"""NASA POWER data validator."""
import pandas as pd
from .base_validator import BaseValidator
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class NASAPOWERValidator(BaseValidator):
    """Validator for NASA POWER climate data."""

    def __init__(self):
        super().__init__("NASAPOWER")

    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate NASA POWER data.

        Args:
            data: DataFrame containing NASA POWER data with columns:
                - latitude, longitude, year, month, day,
                - T2M, T2M_MAX, T2M_MIN, PRECTOTCORR, WS2M, RH2M

        Returns:
            Validation report dictionary.
        """
        if data.empty:
            logger.warning("No NASA POWER data to validate")
            return {
                "source": self.source_name,
                "record_count": 0,
                "validation_passed": False,
                "errors": ["No data to validate"],
                "completeness_score": 0.0,
                "consistency_score": 0.0,
                "plausibility_score": 0.0
            }

        # Define required columns for NASA POWER data
        required_columns = ["latitude", "longitude", "year", "month", "day"]

        # Completeness check
        completeness_result = self._check_completeness(data, required_columns)

        # Consistency checks
        consistency_checks = [
            {"column": "latitude", "condition": "x >= -90 and x <= 90"},
            {"column": "longitude", "condition": "x >= -180 and x <= 180"},
            {"column": "year", "condition": "x >= 1980 and x <= 2030"},
            {"column": "month", "condition": "x >= 1 and x <= 12"},
            {"column": "day", "condition": "x >= 1 and x <= 31"},
            {"column": "T2M", "condition": "x is not None or x == ''"},  # Allow empty for optional
            {"column": "PRECTOTCORR", "condition": "x is not None or x == ''"},
            {"column": "WS2M", "condition": "x is not None or x == ''"},
            {"column": "RH2M", "condition": "x is not None or x == ''"}
        ]
        consistency_result = self._check_consistency(data, consistency_checks)

        # Plausibility checks
        plausibility_rules = [
            {"column": "latitude", "description": "Latitude should be within valid geographic bounds"},
            {"column": "longitude", "description": "Longitude should be within valid geographic bounds"},
            {"column": "year", "description": "Year should be reasonable for POWER data availability"},
            {"column": "month", "description": "Month should be valid calendar month"},
            {"column": "day", "description": "Day should be valid for the given month/year"},
            {"column": "T2M", "description": "Temperature should be within plausible range (-50 to 60°C)"},
            {"column": "PRECTOTCORR", "description": "Precipitation should be non-negative"},
            {"column": "WS2M", "description": "Wind speed should be non-negative"},
            {"column": "RH2M", "description": "Relative humidity should be between 0 and 100%"}
        ]
        plausibility_result = self._check_plausibility(data, plausibility_rules)

        # Determine overall validation status
        validation_passed = (
            completeness_result["completeness_score"] >= 0.9 and
            consistency_result["consistency_score"] >= 0.8 and
            plausibility_result["plausibility_score"] >= 0.0  # Placeholder
        )

        # Compile errors
        errors = []
        if completeness_result["completeness_score"] < 0.9:
            errors.append(f"Completeness check failed: {completeness_result['completeness_score']:.2%}")
        if consistency_result["consistency_score"] < 0.8:
            errors.append(f"Consistency check failed: {consistency_result['consistency_score']:.2%}")
        if plausibility_result["plausibility_score"] < 0.0:  # Placeholder
            errors.append("Plausibility check failed")

        # Add specific failure details
        if completeness_result["missing_counts"]:
            errors.append(f"Missing values in: {list(completeness_result['missing_counts'].keys())}")
        if consistency_result["failed_checks"]:
            failed_checks_desc = []
            for fc in consistency_result["failed_checks"]:
                if "error" in fc:
                    failed_checks_desc.append(f"{fc['check']['column']}: {fc['error']}")
                else:
                    failed_checks_desc.append(f"{fc['check']['column']}: {fc['failed_count']} failed")
            errors.append(f"Failed consistency checks: {', '.join(failed_checks_desc)}")

        logger.info(f"NASA POWER validation completed. Passed: {validation_passed}")

        return {
            "source": self.source_name,
            "record_count": len(data),
            "validation_passed": validation_passed,
            "errors": errors,
            "completeness_score": completeness_result["completeness_score"],
            "consistency_score": consistency_result["consistency_score"],
            "plausibility_score": plausibility_result["plausibility_score"],
            "details": {
                "completeness": completeness_result,
                "consistency": consistency_result,
                "plausibility": plausibility_result
            }
        }
