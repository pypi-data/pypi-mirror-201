"""Module of basic classes in num_collect package."""

from num_collect._cpp_module.num_collect_py_cpp_module import (
    AlgorithmFailure,
    AssertionFailure,
    FileError,
    InvalidArgument,
    NumCollectCppException,
    PreconditionNotSatisfied,
)

all_exports: list = [
    NumCollectCppException,
    AssertionFailure,
    PreconditionNotSatisfied,
    InvalidArgument,
    AlgorithmFailure,
    FileError,
]
for e in all_exports:
    e.__module__ == __name__

__all__ = [e.__name__ for e in all_exports]

del all_exports
del e
