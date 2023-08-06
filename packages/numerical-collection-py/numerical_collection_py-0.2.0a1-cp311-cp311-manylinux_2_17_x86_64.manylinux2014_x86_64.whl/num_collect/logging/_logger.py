"""Module of loggers."""

import datetime
import inspect
import os
import types
import typing

from num_collect._cpp_module.num_collect_py_cpp_module import (
    LogConfig,
    LogLevel,
    LogTagConfig,
)

# For generation of source code information,
# I referred https://github.com/python/cpython/blob/c2bd55d26f8eb2850eb9f9026b5d7f0ed1420b65/Lib/logging/__init__.py.


def tester() -> None:
    """Function for THIS_FILEPATH."""


THIS_FILEPATH = os.path.normcase(tester.__code__.co_filename)


def is_in_this_file(frame: types.FrameType) -> bool:
    """Check whether a frame is in this file.

    Args:
        frame (types.FrameType): Frame.

    Returns:
        bool: Whether the frame is in this file.
    """
    return os.path.normcase(frame.f_code.co_filename) == THIS_FILEPATH


def get_source_info() -> typing.Tuple[str, int, str]:
    """Get the information of the source code for logs.

    Returns:
        typing.Tuple[str, int, str]: File path, line number, and function name.
    """
    frame = inspect.currentframe()

    while True:
        if frame is None:
            file_path = ""
            line = 0
            function_name = ""
            return (file_path, line, function_name)

        if not is_in_this_file(frame):
            break

        frame = frame.f_back

    file_path = frame.f_code.co_filename
    line = frame.f_lineno
    function_name = frame.f_code.co_name
    return (file_path, line, function_name)


class NumCollectLogger:
    """Class of loggers to use logging module in C++.

    Args:
        tag (str): Tag.

    """

    def __init__(
        self,
        tag: typing.Optional[str] = None,
        *,
        config: typing.Optional[LogTagConfig] = None,
    ) -> None:
        if not tag:
            tag = ""
        if not config:
            config = LogConfig.get_config_of(tag)

        self._tag = tag
        self._config = config
        self._sink = self._config.sink

    def log(self, level: LogLevel, message: str, *args: typing.Any) -> None:
        """Write a log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            level (LogLevel): Log level.
            message (str): Message.
        """
        if level < self._config.output_log_level:
            return

        if args:
            body = message % args
        else:
            body = message

        time = datetime.datetime.now()
        file_path, line, function_name = get_source_info()
        column = 0  # Unknown.

        self._sink.write(
            time=time,
            tag=self._tag,
            level=level,
            file_path=file_path,
            line=line,
            column=column,
            function_name=function_name,
            body=body,
        )

    def trace(self, message: str, *args: typing.Any) -> None:
        """Write a trace log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.trace, message, *args)

    def debug(self, message: str, *args: typing.Any) -> None:
        """Write a debug log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.debug, message, *args)

    def iteration(self, message: str, *args: typing.Any) -> None:
        """Write a iteration log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.iteration, message, *args)

    def iteration_label(self, message: str, *args: typing.Any) -> None:
        """Write a iteration_label log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.iteration_label, message, *args)

    def summary(self, message: str, *args: typing.Any) -> None:
        """Write a summary log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.summary, message, *args)

    def info(self, message: str, *args: typing.Any) -> None:
        """Write a info log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.info, message, *args)

    def warning(self, message: str, *args: typing.Any) -> None:
        """Write a warning log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.warning, message, *args)

    def error(self, message: str, *args: typing.Any) -> None:
        """Write a error log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.error, message, *args)

    def critical(self, message: str, *args: typing.Any) -> None:
        """Write a critical log.

        Additional arguments are used for formatting the message
        as in logging.Logger in Python standard library.

        Args:
            message (str): Message.
        """
        self.log(LogLevel.critical, message, *args)
