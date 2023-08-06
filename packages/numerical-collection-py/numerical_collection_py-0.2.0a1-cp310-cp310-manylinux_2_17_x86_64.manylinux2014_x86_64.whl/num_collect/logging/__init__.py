"""Module of logging in num_collect package."""

from num_collect._cpp_module.num_collect_py_cpp_module import (
    LogConfig,
    LogLevel,
    LogSinkBase,
    LogTagConfig,
    load_logging_config_file,
)
from num_collect.logging._handler import NumCollectLogHandler
from num_collect.logging._logger import NumCollectLogger

all_exports: list = [
    LogLevel,
    LogSinkBase,
    LogTagConfig,
    LogConfig,
    NumCollectLogger,
    NumCollectLogHandler,
    load_logging_config_file,
]
for e in all_exports:
    e.__module__ == __name__

__all__ = [e.__name__ for e in all_exports]

del all_exports
del e
