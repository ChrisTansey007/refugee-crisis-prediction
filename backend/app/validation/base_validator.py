"""Base validator for data validation."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import pandas as pd


class BaseValidator(ABC):
    """Abstract base class for data validators."""

    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate the data and return a validation report.

        Args:
            data: The data to validate.

        Returns:
            A dictionary containing validation results.
        """
        pass

    def _check_completeness(self, data: pd.DataFrame, required_columns: List[str]) -> Dict[str, Any]:
        """Check for missing values in required columns."""
        missing_counts = data[required_columns].isnull().sum()
        total_rows = len(data)
        completeness_score = 1.0 - (missing_counts.sum() / (total_rows * len(required_columns))) if total_rows > 0 else 1.0
        return {
            "missing_counts": missing_counts.to_dict(),
            "completeness_score": completeness_score,
            "failed_rows": total_rows - data.dropna(subset=required_columns).shape[0] if total_rows > 0 else 0
        }

    def _check_consistency(self, data: pd.DataFrame, checks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run consistency checks (e.g., value ranges, categorical values)."""
        failed_checks = []
        for check in checks:
            column = check["column"]
            condition = check["condition"]
            if column not in data.columns:
                failed_checks.append({"check": check, "error": f"Column {column} not found"})
                continue
            # Apply condition (this is a simplified example; in practice, condition would be a callable or expression)
            # For now, we assume condition is a string that can be evaluated with `eval` (use with caution in production)
            try:
                # This is a placeholder for actual condition evaluation
                # In a real system, we would use a safe evaluation method or predefined check functions
                passed = data[column].apply(lambda x: eval(condition, {"x": x}) if pd.notnull(x) else True)
                failed_count = (~passed).sum()
                if failed_count > 0:
                    failed_checks.append({"check": check, "failed_count": int(failed_count)})
            except Exception as e:
                failed_checks.append({"check": check, "error": str(e)})
        return {
            "failed_checks": failed_checks,
            "consistency_score": 1.0 - (len(failed_checks) / len(checks)) if checks else 1.0
        }

    def _check_plausibility(self, data: pd.DataFrame, plausibility_rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run plausibility checks (e.g., date ranges, logical constraints)."""
        # Similar to consistency but for domain-specific plausibility
        failed_rules = []
        for rule in plausibility_rules:
            column = rule["column"]
            rule_description = rule["description"]
            # Placeholder for actual plausibility check
            # In practice, this would be a function that evaluates the rule
            failed_rules.append({"rule": rule_description, "error": "Plausibility check not implemented"})
        return {
            "failed_rules": failed_rules,
            "plausibility_score": 0.0  # Placeholder
        }
