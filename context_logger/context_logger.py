import logging
import threading
import uuid
from .context_threading import ContextThread

logger = None


class ContextLogger(logging.Logger):
    """
    A custom logger class that extends the functionality of the standard logging.Logger class.
    """

    def __init__(self, name):
        """
        Initializes the custom logger with a name and sets up thread-local storage for log context.

        :param name: str - The name of the logger.
        """
        super().__init__(name)
        self.local = threading.local()
        self.local.log_context = {}

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
        if self.local.log_context and "requestId" not in self.local.log_context:
            self.local.log_context["requestId"] = str(uuid.uuid4())
        record.log_context = f"{self.local.log_context}"
        return record


def initialize_context_logger(level: str = logging.INFO):
    """
    Initializes the custom logger with the specified log level.

    :param level: str - The log level for the logger.
    """
    global logger
    logging.setLoggerClass(ContextLogger)
    logger = logging.getLogger("custom_logger")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(log_context)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    threading.Thread = ContextThread
