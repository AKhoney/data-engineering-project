"""Retry Logic with Exponential Backoff"""

import time
from typing import Callable, Any, Type, Tuple
from src.config.constants import RETRY_CONFIG
from src.logging.logger import LoggerManager


class ExponentialBackoff:
    """Exponential backoff strategy for retries"""

    def __init__(
        self,
        initial_backoff: int = None,
        max_backoff: int = None,
        multiplier: float = None,
    ):
        self.initial_backoff = initial_backoff or RETRY_CONFIG["initial_backoff_seconds"]
        self.max_backoff = max_backoff or RETRY_CONFIG["max_backoff_seconds"]
        self.multiplier = multiplier or RETRY_CONFIG["backoff_multiplier"]
        self.current_backoff = self.initial_backoff
        self.logger = LoggerManager.get_logger(__name__)

    def get_wait_time(self) -> int:
        """Get current wait time and update for next call"""
        wait_time = self.current_backoff
        self.current_backoff = min(
            int(self.current_backoff * self.multiplier), self.max_backoff
        )
        return wait_time

    def reset(self) -> None:
        """Reset backoff to initial value"""
        self.current_backoff = self.initial_backoff


class RetryHandler:
    """Retry handler with exponential backoff"""

    def __init__(
        self,
        max_retries: int = None,
        backoff: ExponentialBackoff = None,
        retryable_exceptions: Tuple[Type[Exception], ...] = None,
    ):
        self.max_retries = max_retries or RETRY_CONFIG["max_retries"]
        self.backoff = backoff or ExponentialBackoff()
        self.retryable_exceptions = retryable_exceptions or (Exception,)
        self.logger = LoggerManager.get_logger(__name__)

    def execute_with_retry(
        self,
        func: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute function with automatic retry on failure"""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                self.logger.debug(f"Attempt {attempt + 1} of {self.max_retries + 1}")
                result = func(*args, **kwargs)
                self.backoff.reset()
                return result

            except self.retryable_exceptions as e:
                last_exception = e

                if attempt < self.max_retries:
                    wait_time = self.backoff.get_wait_time()
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    # Uncomment for actual implementation:
                    # time.sleep(wait_time)
                else:
                    self.logger.error(
                        f"All {self.max_retries + 1} attempts failed. "
                        f"Last error: {str(e)}"
                    )

        raise last_exception


def retry_decorator(
    max_retries: int = None,
    backoff_strategy: ExponentialBackoff = None,
    retryable_exceptions: Tuple[Type[Exception], ...] = None,
):
    """Decorator for functions that should retry on failure"""

    def decorator(func: Callable) -> Callable:
        handler = RetryHandler(
            max_retries=max_retries,
            backoff=backoff_strategy,
            retryable_exceptions=retryable_exceptions,
        )

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return handler.execute_with_retry(func, *args, **kwargs)

        return wrapper

    return decorator
