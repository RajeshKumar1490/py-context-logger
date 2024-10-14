import logging
import threading
import uuid
from .context_threading import ContextThread

logger = None
_DEFAULT_LOGGER_NAME = "context_logger"
_DEFAULT_LOG_FORMAT = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(log_context)s - %(message)s"
_DEFAULT_LOG_LEVEL = logging.INFO


class ContextLogger(logging.Logger):
    """
    A custom logger class that extends the functionality of the standard logging.Logger class.
    """

    def __init__(
        self,
        name: str = _DEFAULT_LOGGER_NAME,
        log_format: str = _DEFAULT_LOG_FORMAT,
        level: str = _DEFAULT_LOG_LEVEL,
        auto_request_id_generation: bool = True
    ):
        """
        Initializes the custom logger with a name and sets up thread-local storage for log context.

        :param name: str - The name of the logger.
        """
        super().__init__(name)
        self.local = threading.local()
        self.local.log_context = {}
        self.name = name
        self.log_format = log_format
        self.level = level
        self.auto_request_id_generation = auto_request_id_generation

    def initialize_context_logger(self):
        """
        Initializes the custom logger with the specified log level.

        :param level: str - The log level for the logger.
        """
        global logger
        logging.setLoggerClass(ContextLogger)
        logger = logging.getLogger(self.name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(self.log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.level)
        logger.propagate = False
        threading.Thread = ContextThread

    def set_log_context(self, key, value):
        """
        Sets a key-value pair in the log context.

        :param key: str - The key for the log context entry.
        :param value: Any - The value for the log context entry.
        """
        if not hasattr(self.local, "log_context"):
            self.local.log_context = {}
        self.local.log_context[key] = value

    def get_log_context(self):
        """
        Retrieves a copy of the current log context.

        :return: dict - A copy of the log context.
        """
        if not hasattr(self.local, "log_context"):
            self.local.log_context = {}
        return self.local.log_context.copy()

    def update_log_context(self, new_context):
        """
        Updates the log context with a new context.

        :param new_context: dict - The new context to be added to the log context.
        """
        if not hasattr(self.local, "log_context"):
            self.local.log_context = {}
        self.local.log_context.update(new_context)

    def clear_log_context(self):
        """
        Clears the current log context.
        """
        if hasattr(self.local, "log_context"):
            self.local.log_context = {}

    def makeRecord(self, *args, **kwargs):
        """
        Creates a log record with the current log context.

        :return: LogRecord - The created log record.
        """
        record = super().makeRecord(*args, **kwargs)
        if not hasattr(self.local, "log_context"):
            self.local.log_context = {}
        if self.auto_request_id_generation and "logRequestId" not in self.local.log_context:
            self.local.log_context["logRequestId"] = str(uuid.uuid4())
        record.log_context = f"{self.local.log_context}"
        return record

    def get_property_value(self, log_property: str) -> str:
        """
        Retrieve the value associated with a given parameter from the logging context.

        This method checks if a logging context is available. If it is, the method
        attempts to retrieve the value for the specified parameter. If no value is
        found, an empty string is returned.

        Args:
            log_property (str): The name of the log property to retrieve from the logging context.

        Returns:
            str: The value associated with the specified parameter. Returns an empty
            string if the parameter is not found or if the logging context is not available.
        """
        value = ""
        if self.local.log_context:
            value = self.local.log_context.get(log_property, "")
        return value
