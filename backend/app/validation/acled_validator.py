"""ACLED data validator."""
import pandas as pd
from .base_validator import BaseValidator
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ACLEDValidator(BaseValidator):
    """Validator for ACLED conflict data."""

    def __init__(self):
        super().__init__("ACLED")

    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate ACLED data.

        Args:
            data: DataFrame containing ACLED data with columns:
                - data_id, year, time_precision, event_type, sub_event_type,
                - actor1, actor2, association_actor_1, association_actor_2,
                - interaction, country, admin1, admin2, admin3, location,
                - latitude, longitude, geo_precision, source, source_scale,
                - notes, fatalities

        Returns:
            Validation report dictionary.
        """
        if data.empty:
            logger.warning("No ACLED data to validate")
            return {
                "source": self.source_name,
                "record_count": 0,
                "validation_passed": False,
                "errors": ["No data to validate"],
                "completeness_score": 0.0,
                "consistency_score": 0.0,
                "plausibility_score": 0.0
            }

        # Define required columns for ACLED data
        required_columns = [
            "data_id", "year", "event_type", "country", 
            "latitude", "longitude", "fatalities"
        ]

        # Completeness check
        completeness_result = self._check_completeness(data, required_columns)

        # Consistency checks
        consistency_checks = [
            {"column": "year", "condition": "x >= 1997 and x <= 2030"},
            {"column": "latitude", "condition": "x >= -90 and x <= 90"},
            {"column": "longitude", "condition": "x >= -180 and x <= 180"},
            {"column": "fatalities", "condition": "x >= 0"},
            {"column": "event_type", "condition": "x in ['Violence against civilians', 'Battles', 'Explosions/Remote violence', 'Riots', 'Protests', 'Strategic developments']"},
            {"column": "data_id", "condition": "str(x).startswith('event')"}
        ]
        consistency_result = self._check_consistency(data, consistency_checks)

        # Plausibility checks
        plausibility_rules = [
            {"column": "year", "description": "ACLED data starts from 1997"},
            {"column": "latitude", "description": "Latitude should be within valid geographic bounds"},
            {"column": "longitude", "description": "Longitude should be within valid geographic bounds"},
            {"column": "fatalities", "description": "Fatalities should be non-negative"},
            {"column": "country", "description": "Country should be a valid country name"},
            {"column": "data_id", "description": "ACLED event IDs should follow expected format"}
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

        logger.info(f"ACLED validation completed. Passed: {validation_passed}")

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
