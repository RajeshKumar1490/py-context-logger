import logging
import threading
import uuid
from typing import Dict, Union
from .context_threading import ContextThread

logger = None
_DEFAULT_LOGGER_NAME = "context_logger"
_DEFAULT_LOG_FORMAT = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(log_context)s - %(message)s"
_DEFAULT_LOG_LEVEL = logging.INFO


class ContextLogger(logging.Logger):
    """
    A custom logger class that supports thread-local logging context and integrates with GCP logging if enabled.
    """

    def __init__(
        self,
        name: str = _DEFAULT_LOGGER_NAME,
        log_format: str = _DEFAULT_LOG_FORMAT,
        level: Union[str, int] = _DEFAULT_LOG_LEVEL,
        auto_request_id_generation: bool = False
    ):
        """
        Initialize the custom logger.

        Args:
            name (str): Name of the logger.
            log_format (str): Format for log messages.
            level Union[str, int]: Logging level (e.g., logging.INFO / 'INFO').
            auto_request_id_generation (bool): Whether to auto-generate a request ID for each log.
        """
        super().__init__(name)
        self.local = threading.local()
        self.local.log_context = {}
        self.log_format = log_format
        self.level = level
        self.auto_request_id_generation = auto_request_id_generation

    def initialize_context_logger(self) -> "ContextLogger":
        """
        Initialize and configure the logger for use.

        Returns:
            ContextLogger: The configured logger instance.
        """
        global logger
        logging.setLoggerClass(ContextLogger)
        logger = self
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(self.log_format))
        self.propagate = False
        self.setLevel(self.level)
        threading.Thread = ContextThread

        return logger

    def set_log_context(self, key: str, value: str) -> None:
        """
        Sets a key-value pair in the log context.

        :param key: str - The key for the log context entry.
        :param value: Any - The value for the log context entry.
        """
        self._ensure_log_context()
        self.local.log_context[key] = value

    def set_bulk_log_context(self, key_value: Dict[str, str]) -> None:
        """
        Set multiple key-value pairs in the thread-local logging context.

        :param key_value: Dict[str, str] - The key, value pair for the log context entries.
        """
        self._ensure_log_context()
        self.local.log_context.update(key_value)

    def get_log_context(self) -> Dict[str, str]:
        """
        Retrieve the current log context.

        Returns:
            Dict[str, Any]: A copy of the current log context.
        """
        self._ensure_log_context()
        return self.local.log_context.copy()

    def update_log_context(self, new_context: Dict[str, str]) -> None:
        """
        Update the log context with new key-value pairs.

        Args:
            new_context (Dict[str, Any]): New key-value pairs to add to the log context.
        """
        self._ensure_log_context()
        self.local.log_context.update(new_context)

    def clear_log_context(self) -> None:
        """
        Clear the thread-local logging context.
        """
        if hasattr(self.local, "log_context"):
            self.local.log_context = {}

    def makeRecord(self, *args, **kwargs) -> logging.LogRecord:
        """
        Creates a log record with the current log context.

        :return: LogRecord - The created log record.
        """
        record = super().makeRecord(*args, **kwargs)
        self._ensure_log_context()
        if self.auto_request_id_generation and "logRequestId" not in self.local.log_context:
            self.local.log_context["logRequestId"] = str(uuid.uuid4())

        record.log_context = f"{self.local.log_context}"
        return record

    def get_property_value(self, log_property: str) -> str:
        """
        Retrieve a specific property value from the logging context.

        Args:
            log_property (str): The name of the property to retrieve.

        Returns:
            Optional[Any]: The value of the property, or None if not found.
        """
        self._ensure_log_context()
        return self.local.log_context.get(log_property, "")

    def _ensure_log_context(self) -> None:
        """
        Ensure that the log context is initialized for the current thread.
        """
        if self.local and not self.local.get("log_context"):
            self.local.log_context = {}
