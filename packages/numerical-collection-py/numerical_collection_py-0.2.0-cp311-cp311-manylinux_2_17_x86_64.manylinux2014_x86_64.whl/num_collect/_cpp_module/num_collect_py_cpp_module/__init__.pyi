from __future__ import annotations
import num_collect._cpp_module.num_collect_py_cpp_module
import typing
import datetime

__all__ = [
    "AlgorithmFailure",
    "AssertionFailure",
    "FileError",
    "InvalidArgument",
    "LogConfig",
    "LogLevel",
    "LogSinkBase",
    "LogTagConfig",
    "NumCollectCppException",
    "PreconditionNotSatisfied",
    "load_logging_config_file",
    "opt",
]

class NumCollectCppException(RuntimeError, Exception, BaseException):
    pass

class AssertionFailure(NumCollectCppException, RuntimeError, Exception, BaseException):
    pass

class FileError(NumCollectCppException, RuntimeError, Exception, BaseException):
    pass

class InvalidArgument(NumCollectCppException, RuntimeError, Exception, BaseException):
    pass

class LogConfig:
    """
    Class of configurations of logs.
    """

    @staticmethod
    def get_config_of(tag: str) -> LogTagConfig:
        """
        Get the configuration of a tag.

        Args:
            tag (str): Tag.

        Returns:
            LogTagConfig: Configuration.
        """
    @staticmethod
    def get_default_tag_config() -> LogTagConfig:
        """
        Get the default configuration of log tags.

        Returns:
            LogTagConfig: Default configuration of log tags.
        """
    @staticmethod
    def set_config_of(tag: str, config: LogTagConfig) -> None:
        """
        Set the configuration of a tag.

        Args:
            tag (str): Tag.
            config (LogTagConfig): Configuration.
        """
    @staticmethod
    def set_default_tag_config(config: LogTagConfig) -> None:
        """
        Set the default configuration of log tags.

        Args:
            config (LogTagConfig): Configuration.
        """
    pass

class LogLevel:
    """
    Enumeration of log levels.

    Members:

      trace : For internal trace logs.

      debug : For debug information. (Meant for use in user code, not in algorithms.)

      iteration : For logs of iterations.

      iteration_label : For labels of iteration logs.

      summary : For summary of calculations.

      info : For some information. (Meant for use in user code, not in algorithms.)

      warning : For warnings.

      error : For errors.

      critical : For critical errors.

      off : Turn off output (only for output log level).
    """

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'trace': <LogLevel.trace: 0>, 'debug': <LogLevel.debug: 1>, 'iteration': <LogLevel.iteration: 2>, 'iteration_label': <LogLevel.iteration_label: 3>, 'summary': <LogLevel.summary: 4>, 'info': <LogLevel.info: 5>, 'warning': <LogLevel.warning: 6>, 'error': <LogLevel.error: 7>, 'critical': <LogLevel.critical: 8>, 'off': <LogLevel.off: 9>}
    critical: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.critical: 8>
    debug: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.debug: 1>
    error: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.error: 7>
    info: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.info: 5>
    iteration: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.iteration: 2>
    iteration_label: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.iteration_label: 3>
    off: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.off: 9>
    summary: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.summary: 4>
    trace: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.trace: 0>
    warning: num_collect._cpp_module.num_collect_py_cpp_module.LogLevel  # value = <LogLevel.warning: 6>
    pass

class LogSinkBase:
    """
    Interface of log sinks.
    """

    def __init__(self) -> None: ...
    def write(
        self,
        time: datetime.datetime,
        tag: str,
        level: LogLevel,
        file_path: str,
        line: int,
        column: int,
        function_name: str,
        body: str,
    ) -> None:
        """
        Write a log.

        Args:
            time (datetime.datetime): Time.
            tag (str): Tag.
            level (LogLevel): Log level.
            file_path (str): File path.
            line (int): Line number in the file.
            column (int): Column number in the line.
            function_name (str): Function name.
            body (str): Log body.
        """
    pass

class LogTagConfig:
    """
    Class to hold configurations for log tags.
    """

    def __init__(self) -> None: ...
    @property
    def iteration_label_period(self) -> int:
        """
        Period to write labels of iteration logs.

        :type: int
        """
    @iteration_label_period.setter
    def iteration_label_period(self, arg1: int) -> None:
        """
        Period to write labels of iteration logs.
        """
    @property
    def iteration_output_period(self) -> int:
        """
        Period to write iteration logs.

        :type: int
        """
    @iteration_output_period.setter
    def iteration_output_period(self, arg1: int) -> None:
        """
        Period to write iteration logs.
        """
    @property
    def output_log_level(self) -> LogLevel:
        """
        Minimum log level to output.

        :type: LogLevel
        """
    @output_log_level.setter
    def output_log_level(self, arg1: LogLevel) -> None:
        """
        Minimum log level to output.
        """
    @property
    def output_log_level_in_child_iterations(self) -> LogLevel:
        """
        Minimum log level to output in child iterations.

        :type: LogLevel
        """
    @output_log_level_in_child_iterations.setter
    def output_log_level_in_child_iterations(self, arg1: LogLevel) -> None:
        """
        Minimum log level to output in child iterations.
        """
    @property
    def sink(self) -> LogSinkBase:
        """
        Log sink.

        :type: LogSinkBase
        """
    @sink.setter
    def sink(self, arg1: LogSinkBase) -> None:
        """
        Log sink.
        """
    pass

class AlgorithmFailure(NumCollectCppException, RuntimeError, Exception, BaseException):
    pass

class PreconditionNotSatisfied(
    NumCollectCppException, RuntimeError, Exception, BaseException
):
    pass

def load_logging_config_file(file_path: str) -> None:
    """
    Parse and apply configurations of logging from a file.

    Args:
        file_path (str): File path.
    """
