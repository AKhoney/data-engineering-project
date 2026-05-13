"""Archive Management for Data Lifecycle"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

from src.config.config import Config
from src.config.constants import ARCHIVE_SCHEDULE
from src.logging.logger import LoggerManager


class ArchiveFrequency(Enum):
    """Archive frequency options"""
    MONTHLY = "month-end"
    WEEKLY = "weekend"
    DAILY = "daily"


class ArchiveManager:
    """Manages data archival and original/archive table synchronization"""

    def __init__(self, frequency: str = None):
        self.frequency = frequency or Config.ARCHIVE_FREQUENCY
        self.retention_days = Config.ARCHIVE_RETENTION_DAYS
        self.logger = LoggerManager.get_logger(__name__)

    def should_archive_today(self) -> bool:
        """Determine if archival should happen today"""
        today = datetime.now()

        if self.frequency == ArchiveFrequency.DAILY.value:
            return True

        elif self.frequency == ArchiveFrequency.MONTHLY.value:
            # Check if today is month-end
            tomorrow = today + timedelta(days=1)
            return today.month != tomorrow.month

        elif self.frequency == ArchiveFrequency.WEEKLY.value:
            # Check if today is weekend
            return today.weekday() >= 5  # 5 = Saturday, 6 = Sunday

        return False

    def get_next_archive_date(self) -> datetime:
        """Get the next scheduled archive date"""
        today = datetime.now()

        if self.frequency == ArchiveFrequency.DAILY.value:
            return today + timedelta(days=1)

        elif self.frequency == ArchiveFrequency.MONTHLY.value:
            # Next month-end
            if today.month == 12:
                return datetime(today.year + 1, 1, 1) - timedelta(days=1)
            else:
                return datetime(today.year, today.month + 1, 1) - timedelta(days=1)

        elif self.frequency == ArchiveFrequency.WEEKLY.value:
            # Next Saturday
            days_until_saturday = (5 - today.weekday()) % 7
            if days_until_saturday == 0:
                days_until_saturday = 7
            return today + timedelta(days=days_until_saturday)

        return None

    def generate_archive_instructions(
        self, table_name: str, layer: str
    ) -> Dict[str, Any]:
        """Generate SQL/commands for archival process"""
        archive_table = f"{table_name}_archive"
        original_table = f"{table_name}_original"

        return {
            "step_1_copy_to_archive": {
                "description": "Append current original data to archive",
                "operation": "INSERT INTO",
                "source_table": original_table,
                "target_table": archive_table,
                "mode": "APPEND",
            },
            "step_2_add_metadata": {
                "description": "Add archive metadata (timestamp, layer)",
                "columns_to_add": {
                    "archived_at": datetime.utcnow().isoformat(),
                    "archive_layer": layer,
                    "archive_batch_id": self._generate_batch_id(),
                },
            },
            "step_3_clear_original": {
                "description": "Clear original table for fresh data",
                "operation": "DELETE FROM",
                "target_table": original_table,
                "condition": "1=1",  # Delete all records
            },
            "step_4_validate": {
                "description": "Validate archival success",
                "checks": [
                    f"Verify archive row count > 0",
                    f"Verify original table is empty",
                    f"Verify metadata columns populated",
                ],
            },
        }

    def get_cleanup_instructions(self) -> Dict[str, Any]:
        """Get instructions for cleaning old archive data based on retention"""
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)

        return {
            "retention_period_days": self.retention_days,
            "cutoff_date": cutoff_date.isoformat(),
            "action": "DELETE",
            "condition": f"archived_at < '{cutoff_date.isoformat()}'",
            "note": f"Archives older than {self.retention_days} days will be deleted",
        }

    def log_archive_event(
        self,
        table_name: str,
        status: str,
        records_archived: int = 0,
        details: Dict[str, Any] = None,
    ) -> None:
        """Log archive operation"""
        LoggerManager.log_pipeline_event(
            self.logger,
            event_type="archive_operation",
            status=status,
            table_name=table_name,
            records_archived=records_archived,
            timestamp=datetime.utcnow().isoformat(),
            details=details,
        )

    @staticmethod
    def _generate_batch_id() -> str:
        """Generate unique batch ID for archive operation"""
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    def get_archive_strategy_summary(self) -> Dict[str, Any]:
        """Get summary of archive strategy"""
        return {
            "frequency": self.frequency,
            "retention_period_days": self.retention_days,
            "next_archive_date": str(self.get_next_archive_date()),
            "archive_pattern": {
                "current_data": "original_table (DELETE + INSERT)",
                "historical_data": "archive_table (APPEND ONLY)",
                "updates": "Cannot update archive data (append-only pattern)",
            },
            "benefits": [
                "Full historical tracking",
                "Point-in-time recovery",
                "Immutable audit trail",
                "Easy compliance reporting",
            ],
        }
