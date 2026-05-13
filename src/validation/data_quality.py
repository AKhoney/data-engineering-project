"""Data Quality Validation Framework"""

from typing import Dict, List, Any, Tuple
from datetime import datetime
from src.config.constants import DATA_QUALITY_THRESHOLDS
from src.logging.logger import LoggerManager


class DataQualityValidator:
    """Framework for validating data quality"""

    def __init__(self):
        self.logger = LoggerManager.get_logger(__name__)
        self.checks_passed = 0
        self.checks_failed = 0
        self.validation_results = []

    def validate_row_count(
        self, record_count: int, min_expected: int = None
    ) -> Tuple[bool, str]:
        """Validate minimum row count"""
        min_expected = min_expected or DATA_QUALITY_THRESHOLDS["min_row_count"]

        if record_count < min_expected:
            self.checks_failed += 1
            msg = f"Row count {record_count} below threshold {min_expected}"
            self._log_check("row_count", False, msg)
            return False, msg

        self.checks_passed += 1
        msg = f"Row count {record_count} is acceptable"
        self._log_check("row_count", True, msg)
        return True, msg

    def validate_null_percentage(
        self, null_count: int, total_count: int, max_null_pct: float = None
    ) -> Tuple[bool, str]:
        """Validate null value percentage"""
        max_null_pct = max_null_pct or DATA_QUALITY_THRESHOLDS["max_null_percentage"]

        if total_count == 0:
            return False, "Total count is zero"

        null_percentage = (null_count / total_count) * 100

        if null_percentage > max_null_pct:
            self.checks_failed += 1
            msg = f"Null percentage {null_percentage:.2f}% exceeds threshold {max_null_pct}%"
            self._log_check("null_percentage", False, msg)
            return False, msg

        self.checks_passed += 1
        msg = f"Null percentage {null_percentage:.2f}% is acceptable"
        self._log_check("null_percentage", True, msg)
        return True, msg

    def validate_duplicates(
        self, total_count: int, unique_count: int, threshold: float = None
    ) -> Tuple[bool, str]:
        """Validate duplicate records"""
        threshold = threshold or DATA_QUALITY_THRESHOLDS["duplicate_threshold"]

        if total_count == 0:
            return False, "Total count is zero"

        duplicate_percentage = ((total_count - unique_count) / total_count) * 100

        if duplicate_percentage > threshold:
            self.checks_failed += 1
            msg = f"Duplicate percentage {duplicate_percentage:.2f}% exceeds threshold {threshold}%"
            self._log_check("duplicates", False, msg)
            return False, msg

        self.checks_passed += 1
        msg = f"No duplicates found"
        self._log_check("duplicates", True, msg)
        return True, msg

    def validate_numeric_range(
        self, values: List[float], min_val: float = None, max_val: float = None
    ) -> Tuple[bool, str]:
        """Validate numeric values are within range"""
        if not values:
            return False, "No values to validate"

        out_of_range = [v for v in values if (min_val and v < min_val) or (max_val and v > max_val)]

        if out_of_range:
            self.checks_failed += 1
            msg = f"{len(out_of_range)} values out of range [{min_val}, {max_val}]"
            self._log_check("numeric_range", False, msg)
            return False, msg

        self.checks_passed += 1
        msg = f"All values within range [{min_val}, {max_val}]"
        self._log_check("numeric_range", True, msg)
        return True, msg

    def validate_temperature(self, temperatures: List[float]) -> Tuple[bool, str]:
        """Validate temperature values"""
        temp_range = DATA_QUALITY_THRESHOLDS["temperature_range"]
        return self.validate_numeric_range(
            temperatures, min_val=temp_range[0], max_val=temp_range[1]
        )

    def validate_humidity(self, humidity_values: List[float]) -> Tuple[bool, str]:
        """Validate humidity values (should be 0-100)"""
        humidity_range = DATA_QUALITY_THRESHOLDS["humidity_range"]
        return self.validate_numeric_range(
            humidity_values, min_val=humidity_range[0], max_val=humidity_range[1]
        )

    def validate_schema(self, data: Dict[str, Any], expected_schema: Dict[str, type]) -> Tuple[bool, str]:
        """Validate data against expected schema"""
        missing_fields = [field for field in expected_schema if field not in data]

        if missing_fields:
            self.checks_failed += 1
            msg = f"Missing required fields: {missing_fields}"
            self._log_check("schema", False, msg)
            return False, msg

        type_mismatches = []
        for field, expected_type in expected_schema.items():
            if field in data and not isinstance(data[field], expected_type):
                type_mismatches.append(f"{field} (expected {expected_type.__name__})")

        if type_mismatches:
            self.checks_failed += 1
            msg = f"Type mismatches: {type_mismatches}"
            self._log_check("schema", False, msg)
            return False, msg

        self.checks_passed += 1
        msg = "Schema validation passed"
        self._log_check("schema", True, msg)
        return True, msg

    def get_validation_report(self) -> Dict[str, Any]:
        """Generate validation report"""
        total_checks = self.checks_passed + self.checks_failed
        pass_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_checks": total_checks,
            "passed": self.checks_passed,
            "failed": self.checks_failed,
            "pass_rate": pass_rate,
            "status": "PASSED" if self.checks_failed == 0 else "FAILED",
        }

    def _log_check(self, check_name: str, passed: bool, message: str) -> None:
        """Log individual check result"""
        self.validation_results.append({
            "check_name": check_name,
            "passed": passed,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        })

        level = "info" if passed else "warning"
        getattr(self.logger, level)(f"[{check_name}] {message}")
