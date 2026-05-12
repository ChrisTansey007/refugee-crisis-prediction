"""World Bank data validator."""
import pandas as pd
from .base_validator import BaseValidator
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class WorldBankValidator(BaseValidator):
    """Validator for World Bank indicator data."""

    def __init__(self):
        super().__init__("WorldBank")

    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate World Bank data.

        Args:
            data: DataFrame containing World Bank data with columns:
                - country_iso, country_name, indicator_code, indicator_name,
                - year, value, unit

        Returns:
            Validation report dictionary.
        """
        if data.empty:
            logger.warning("No World Bank data to validate")
            return {
                "source": self.source_name,
                "record_count": 0,
                "validation_passed": False,
                "errors": ["No data to validate"],
                "completeness_score": 0.0,
                "consistency_score": 0.0,
                "plausibility_score": 0.0
            }

        # Define required columns for World Bank data
        required_columns = ["country_iso", "country_name", "indicator_code", "year", "value"]

        # Completeness check
        completeness_result = self._check_completeness(data, required_columns)

        # Consistency checks
        consistency_checks = [
            {"column": "year", "condition": "x >= 1960 and x <= 2030"},
            {"column": "country_iso", "condition": "len(str(x)) == 3 and str(x).isalpha()"},
            {"column": "value", "condition": "x is not None"}  # Will be handled separately
        ]
        consistency_result = self._check_consistency(data, consistency_checks)

        # Additional value validation (since null check is special)
        null_values = data["value"].isnull().sum()
        if null_values > 0:
            consistency_result["failed_checks"].append({
                "check": {"column": "value", "condition": "x is not None"},
                "failed_count": int(null_values)
            })
            consistency_result["consistency_score"] = 1.0 - (len(consistency_result["failed_checks"]) / 3) if 3 > 0 else 1.0

        # Plausibility checks
        plausibility_rules = [
            {"column": "year", "description": "Year should be reasonable for current context"},
            {"column": "value", "description": "Value should be within plausible range for indicator"},
            {"column": "country_iso", "description": "Country code should be valid ISO3"}
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
        if null_values > 0:
            errors.append(f"Found {null_values} null values in 'value' column")

        logger.info(f"World Bank validation completed. Passed: {validation_passed}")

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
