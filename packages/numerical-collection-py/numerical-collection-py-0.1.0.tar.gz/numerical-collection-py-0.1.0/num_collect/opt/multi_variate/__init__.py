"""Module of optimization algorithms for multi-variate objective functions."""

from num_collect._cpp_module.num_collect_py_cpp_module.opt.multi_variate import (
    AdaptiveDiagonalCurves,
    DividingRectangles,
    DownhillSimplex,
    ObjectiveFunctionBase,
)

all_exports: list = [
    AdaptiveDiagonalCurves,
    DividingRectangles,
    DownhillSimplex,
    ObjectiveFunctionBase,
]
for e in all_exports:
    e.__module__ == __name__

__all__ = [e.__name__ for e in all_exports]

del all_exports
del e
