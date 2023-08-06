"""Module of test problems of optimization algorithms for multi-variate objective functions."""

from num_prob_collect.opt.multi_variate._quadratic_function import QuadraticFunction

all_exports: list = [
    QuadraticFunction,
]
for e in all_exports:
    e.__module__ == __name__

__all__ = [e.__name__ for e in all_exports]

del all_exports
del e
