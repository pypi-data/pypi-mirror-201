"""Module of quadratic function for test of optimization."""

import numpy

import num_collect.opt.multi_variate


class QuadraticFunction(num_collect.opt.multi_variate.ObjectiveFunctionBase):
    """Quadratic function for test of optimization."""

    def __init__(self, *, coeff: float = 3.0) -> None:
        super().__init__()

        self.coeff = coeff

    def evaluate_on(self, var: numpy.ndarray) -> None:
        """Evaluate this objective function on a variable.

        Args:
            var (numpy.ndarray): Variable.
        """
        self.value = self.coeff * numpy.sum(numpy.square(var))
