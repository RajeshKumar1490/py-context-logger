import threading


class ContextThread(threading.Thread):
    """
    A thread class that propagates the log context to the new thread.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the thread with the current log context.

        :param args: list - The positional arguments for the thread.
        :param kwargs: dict - The keyword arguments for the thread.
        """
        from .context_logger import logger
        self.log_context = logger.get_log_context()
        super().__init__(*args, **kwargs)

    def run(self):
        """
        Updates the log context in the new thread before running.
        """
        from .context_logger import logger
        logger.update_log_context(self.log_context)
        super().run()
