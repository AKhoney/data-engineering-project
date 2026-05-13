"""Structured Logging Module with JSON format support"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from pythonjsonlogger import jsonlogger

from src.config.config import Config


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging"""

    def add_fields(
        self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["environment"] = Config.ENVIRONMENT
        log_record["level"] = record.levelname


class LoggerManager:
    """Centralized logger management"""

    _loggers: Dict[str, logging.Logger] = {}

    @staticmethod
    def get_logger(name: str, level: str = None) -> logging.Logger:
        """Get or create a logger instance"""
        if name not in LoggerManager._loggers:
            logger = logging.getLogger(name)
            level = level or Config.LOG_LEVEL

            # Set log level
            logger.setLevel(getattr(logging, level.upper()))

            # Remove default handlers
            logger.handlers = []

            # Add console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.upper()))

            if Config.LOG_FORMAT.lower() == "json":
                formatter = CustomJsonFormatter(
                    "%(timestamp)s %(name)s %(levelname)s %(message)s"
                )
            else:
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )

            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            LoggerManager._loggers[name] = logger

        return LoggerManager._loggers[name]

    @staticmethod
    def log_pipeline_event(
        logger: logging.Logger,
        event_type: str,
        status: str,
        details: Dict[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        """Log pipeline events with structured information"""
        log_entry = {
            "event_type": event_type,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }
        if details:
            log_entry["details"] = details

        logger.info(json.dumps(log_entry))

    @staticmethod
    def log_error_with_context(
        logger: logging.Logger,
        error: Exception,
        context: Dict[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        """Log errors with context information"""
        error_entry = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }
        if context:
            error_entry["context"] = context

        logger.error(json.dumps(error_entry))

    @staticmethod
    def log_data_quality_check(
        logger: logging.Logger,
        check_name: str,
        passed: bool,
        records_processed: int,
        records_failed: int = 0,
        **kwargs: Any,
    ) -> None:
        """Log data quality check results"""
        quality_entry = {
            "check_name": check_name,
            "passed": passed,
            "records_processed": records_processed,
            "records_failed": records_failed,
            "pass_rate": (
                ((records_processed - records_failed) / records_processed * 100)
                if records_processed > 0
                else 0
            ),
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }

        level = "info" if passed else "warning"
        getattr(logger, level)(json.dumps(quality_entry))


# Create module-level logger
logger = LoggerManager.get_logger(__name__)
