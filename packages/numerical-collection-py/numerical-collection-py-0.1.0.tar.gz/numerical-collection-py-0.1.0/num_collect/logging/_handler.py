"""Module of handlers of logs."""


import datetime
import logging

from num_collect._cpp_module.num_collect_py_cpp_module import LogLevel, LogSinkBase


class NumCollectLogHandler(logging.Handler):
    """Class to write logs using log sinks in C++.

    Args:
        sink (LogSinkBase): Log sink.
    """

    def __init__(self, sink: LogSinkBase) -> None:
        super().__init__()

        self._sink = sink

        # Internally uses formatters in logging module to format exceptions.
        self._formatter = logging.Formatter()

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log.

        Args:
            record (logging.LogRecord): Log record.
        """
        self._sink.write(
            time=datetime.datetime.now(),
            tag=record.name,
            level=self._convert_log_level(record.levelno),  # cspell: ignore levelno
            file_path=record.pathname,
            line=record.lineno,
            column=0,  # Unknown.
            function_name=record.funcName,
            body=self._format_body(record),
        )

    def _format_body(self, record: logging.LogRecord) -> str:
        """Format log body.

        Args:
            record (logging.LogRecord): Log record.

        Returns:
            str: Log body for log sinks in C++.
        """
        body = record.getMessage()

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self._formatter.formatException(record.exc_info)
        if record.exc_text:
            if body[-1:] != "\n":
                body = body + "\n"
            body = body + record.exc_text + "\n"

        if record.stack_info:
            if body[-1:] != "\n":
                body = body + "\n"
            body = body + self._formatter.formatStack(record.stack_info) + "\n"

        return body

    def _convert_log_level(self, level: int) -> LogLevel:
        """Convert a log level.

        Args:
            level (int): Log level in logging module.

        Returns:
            LogLevel: Log level in num_collect.
        """
        if level == logging.DEBUG:
            return LogLevel.debug
        if level == logging.INFO:
            return LogLevel.info
        if level == logging.WARNING:
            return LogLevel.warning
        if level == logging.ERROR:
            return LogLevel.error
        if level == logging.CRITICAL:
            return LogLevel.critical
        return LogLevel.trace
