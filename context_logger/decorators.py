import functools
from inspect import signature, isfunction
import logging
import threading


class UseContextLogger:
    """
    A decorator class that sets and updates the log context for functions and classes.
    """

    def __init__(self, log_context=None):
        """
        Initializes the decorator with an optional log context.

        :param log_context: dict - The log context to be set or updated.
        """
        self.log_context = log_context if log_context else {}

    def __call__(self, target):
        """
        Applies the decorator to a function or class.

        :param target: function or class - The target to be decorated.
        :return: function or class - The decorated target.
        """
        if isfunction(target):
            return self.decorate_function(target)
        else:
            return self.decorate_class(target)

    @staticmethod
    def get_nested_value(data, keys):
        """
        Retrieves a nested value from a dictionary using a list of keys.

        :param data: dict - The dictionary to retrieve the value from.
        :param keys: list - The list of keys to traverse the dictionary.
        :return: Any - The retrieved value or None if not found.
        """
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, None)
            else:
                return None
            if data is None:
                break
        return data

    def update_log_context(self, logger, func, bound_args):
        """
        Updates the log context based on specified parameters.

        :param logger: CustomLogger - The logger instance.
        :param func: function - The function being decorated.
        :param bound_args: BoundArguments - The bound arguments of the function.
        """
        new_context = {}
        for param_name, property_name in self.log_context.items():
            keys = param_name.split(".")
            outer_key = keys[0]
            if outer_key in bound_args.arguments:
                nested_value = self.get_nested_value(
                    bound_args.arguments[outer_key], keys[1:]
                )
                if nested_value is not None:
                    new_context[property_name] = nested_value
            elif param_name in bound_args.arguments:
                new_context[property_name] = bound_args.arguments[param_name]
        logger.update_log_context(new_context)

    def decorate_function(self, func):
        """
        Decorates a function to update and bind the log context.

        :param func: function - The function to be decorated.
        :return: function - The decorated function.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("custom_logger")

            # Retrieve function signature and arguments
            sig = signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Update log context based on specified parameters
            self.update_log_context(logger, func, bound_args)

            # Bind logger to the method's local scope
            kwargs["logger"] = logger

            # Wrap thread targets to ensure log context propagation
            for arg_name, arg_value in bound_args.arguments.items():
                if isinstance(arg_value, threading.Thread):
                    context = logger.get_log_context()
                    arg_value._target = self.wrap_thread_target(
                        arg_value._target, context
                    )

            result = func(*args, **kwargs)

            return result

        return wrapper

    def decorate_class(self, cls):
        """
        Decorates a class to update and bind the log context for its methods.

        :param cls: class - The class to be decorated.
        :return: class - The decorated class.
        """

        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("custom_logger")

            # Retrieve function signature and arguments
            sig = signature(cls)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Update log context based on specified parameters
            self.update_log_context(logger, cls, bound_args)

            # Bind logger to the method's local scope
            kwargs["logger"] = logger

            # Wrap thread targets to ensure log context propagation
            for arg_name, arg_value in bound_args.arguments.items():
                if isinstance(arg_value, threading.Thread):
                    context = logger.get_log_context()
                    arg_value._target = self.wrap_thread_target(
                        arg_value._target, context
                    )

            result = cls(*args, **kwargs)

            return result

        return wrapper

    def wrap_thread_target(self, target, context):
        """
        Wraps a thread target to ensure log context propagation.

        :param target: function - The thread target function.
        :param context: dict - The log context to be propagated.
        :return: function - The wrapped thread target function.
        """

        @functools.wraps(target)
        def wrapped(*args, **kwargs):
            logger = logging.getLogger("custom_logger")
            logger.update_log_context(context)
            return target(*args, **kwargs)

        return wrapped


class ClearLogContext:
    """
    A decorator class that clears the log context before executing the decorated function.
    """

    def __call__(self, target):
        """
        Applies the decorator to a function.

        :param target: function - The target to be decorated.
        :return: function - The decorated function.
        """
        return self.decorate_function(target)

    def decorate_function(self, func):
        """
        Decorates a function to clear the log context before execution.

        :param func: function - The function to be decorated.
        :return: function - The decorated function.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("custom_logger")

            # Clear the log context
            logger.clear_log_context()

            result = func(*args, **kwargs)

            return result

        return wrapper
