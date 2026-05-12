"""UNHCR data validator."""
import pandas as pd
from .base_validator import BaseValidator
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class UNHCRValidator(BaseValidator):
    """Validator for UNHCR refugee data."""

    def __init__(self):
        super().__init__("UNHCR")

    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate UNHCR data.

        Args:
            data: DataFrame containing UNHCR data with columns:
                - year, country_of_origin, country_of_origin_iso,
                - country_of_asylum, country_of_asylum_iso,
                - refugees, asylum_seekers, idps, returnees, stateless

        Returns:
            Validation report dictionary.
        """
        if data.empty:
            logger.warning("No UNHCR data to validate")
            return {
                "source": self.source_name,
                "record_count": 0,
                "validation_passed": False,
                "errors": ["No data to validate"],
                "completeness_score": 0.0,
                "consistency_score": 0.0,
                "plausibility_score": 0.0
            }

        # Define required columns for UNHCR data
        required_columns = [
            "year", "country_of_origin", "country_of_origin_iso",
            "country_of_asylum", "country_of_asylum_iso",
            "refugees", "asylum_seekers", "idps", "returnees", "stateless"
        ]

        # Completeness check
        completeness_result = self._check_completeness(data, required_columns)

        # Consistency checks
        consistency_checks = [
            {"column": "year", "condition": "x >= 1950 and x <= 2030"},
            {"column": "refugees", "condition": "x >= 0"},
            {"column": "asylum_seekers", "condition": "x >= 0"},
            {"column": "idps", "condition": "x >= 0"},
            {"column": "returnees", "condition": "x >= 0"},
            {"column": "stateless", "condition": "x >= 0"},
            {"column": "country_of_origin_iso", "condition": "len(str(x)) == 3 and str(x).isalpha()"},
            {"column": "country_of_asylum_iso", "condition": "len(str(x)) == 3 and str(x).isalpha()"}
        ]
        consistency_result = self._check_consistency(data, consistency_checks)

        # Plausibility checks
        plausibility_rules = [
            {"column": "year", "description": "Year should be reasonable for current context"},
            {"column": "refugees", "description": "Refugee count should not exceed world population (~8B)"},
            {"column": "asylum_seekers", "description": "Asylum seeker count should be reasonable"},
            {"column": "idps", "description": "IDP count should be reasonable"},
            {"column": "returnees", "description": "Returnee count should be reasonable"},
            {"column": "stateless", "description": "Stateless count should be reasonable"}
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
            errors.append(f"Failed consistency checks: {[c['check'] for c in consistency_result['failed_checks']]}")

        logger.info(f"UNHCR validation completed. Passed: {validation_passed}")

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
