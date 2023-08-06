from __future__ import annotations
import num_collect._cpp_module.num_collect_py_cpp_module.opt.multi_variate
import typing
import numpy

__all__ = [
    "AdaptiveDiagonalCurves",
    "DividingRectangles",
    "DownhillSimplex",
    "ObjectiveFunctionBase",
]

class AdaptiveDiagonalCurves:
    """
    Class of adaptive diagonal curves (ADC) method :cite:`Sergeyev2006` for optimization.

    Args:
        obj_fun (num_collect.opt.multi_variate.ObjectiveFunctionBase): Objective function.
    """

    def __init__(self, obj_fun: ObjectiveFunctionBase) -> None: ...
    def decrease_rate_bound(self, value: float) -> AdaptiveDiagonalCurves:
        """
        Set the rate of function value used to check whether the function value decreased in the current phase.

        Args:
            value (float): Value.
        """
    def init(self, lower: numpy.ndarray, upper: numpy.ndarray) -> None:
        """
        Initialize the algorithm.

        Args:
            lower (numpy.ndarray): Lower limit of the range of variables.
            upper (numpy.ndarray): Upper limit of the range of variables.
        """
    def is_stop_criteria_satisfied(self) -> None:
        """
        Determine if stopping criteria of the algorithm are satisfied.

        Returns:
            bool: True if stopping criteria of the algorithm are satisfied.
        """
    def iterate(self) -> None:
        """
        Iterate once.

        Note:
            Any required initializations (with init functions) are
            assumed to have been done.
        """
    def max_evaluations(self, value: int) -> AdaptiveDiagonalCurves:
        """
        Set the maximum number of function evaluations.

        Args:
            value (int): Value.
        """
    def min_rate_imp(self, value: float) -> AdaptiveDiagonalCurves:
        """
        Set the minimum rate of improvement in the function value required for potentially optimal rectangles.

        Args:
            value (float): Value.
        """
    def solve(self) -> None:
        """
        Solve the problem.

        Iterate the algorithm until the stopping criteria are satisfied.

        Note:
            Any required initializations (with init functions) are
            assumed to have been done.
        """
    @property
    def evaluations(self) -> int:
        """
        Number of function evaluations.

        :type: int
        """
    @property
    def iterations(self) -> int:
        """
        Number of iterations.

        :type: int
        """
    @property
    def opt_value(self) -> float:
        """
        Current optimal value.

        :type: float
        """
    @property
    def opt_variable(self) -> numpy.ndarray:
        """
        Current optimal variable.

        :type: numpy.ndarray
        """
    pass

class DividingRectangles:
    """
    Class of dividing rectangles (DIRECT) method :cite:`Jones1993` for optimization.

    Args:
        obj_fun (num_collect.opt.multi_variate.ObjectiveFunctionBase): Objective function.
    """

    def __init__(self, obj_fun: ObjectiveFunctionBase) -> None: ...
    def init(self, lower: numpy.ndarray, upper: numpy.ndarray) -> None:
        """
        Initialize the algorithm.

        Args:
            lower (numpy.ndarray): Lower limit of the range of variables.
            upper (numpy.ndarray): Upper limit of the range of variables.
        """
    def is_stop_criteria_satisfied(self) -> None:
        """
        Determine if stopping criteria of the algorithm are satisfied.

        Returns:
            bool: True if stopping criteria of the algorithm are satisfied.
        """
    def iterate(self) -> None:
        """
        Iterate once.

        Note:
            Any required initializations (with init functions) are
            assumed to have been done.
        """
    def max_evaluations(self, value: int) -> DividingRectangles:
        """
        Set the maximum number of function evaluations.

        Args:
            value (int): Value.
        """
    def min_rate_imp(self, value: float) -> DividingRectangles:
        """
        Set the minimum rate of improvement in the function value required for potentially optimal rectangles.

        Args:
            value (float): Value.
        """
    def solve(self) -> None:
        """
        Solve the problem.

        Iterate the algorithm until the stopping criteria are satisfied.

        Note:
            Any required initializations (with init functions) are
            assumed to have been done.
        """
    @property
    def evaluations(self) -> int:
        """
        Number of function evaluations.

        :type: int
        """
    @property
    def iterations(self) -> int:
        """
        Number of iterations.

        :type: int
        """
    @property
    def opt_value(self) -> float:
        """
        Current optimal value.

        :type: float
        """
    @property
    def opt_variable(self) -> numpy.ndarray:
        """
        Current optimal variable.

        :type: numpy.ndarray
        """
    pass

class DownhillSimplex:
    """
    Class of downhill simplex method :cite:`Press2007`.

    Args:
        obj_fun (num_collect.opt.multi_variate.ObjectiveFunctionBase): Objective function.
    """

    def __init__(self, obj_fun: ObjectiveFunctionBase) -> None: ...
    def init(self, init_var: numpy.ndarray, *, width: float = 0.1) -> None:
        """
        Initialize the algorithm.

        Args:
            init_var (numpy.ndarray): Initial variable.
            width (float, optional): Width of the initial simplex.
        """
    def is_stop_criteria_satisfied(self) -> None:
        """
        Determine if stopping criteria of the algorithm are satisfied.

        Returns:
            bool: True if stopping criteria of the algorithm are satisfied.
        """
    def iterate(self) -> None:
        """
        Iterate once.

        Note:
            Any required initializations (with init functions) are
            assumed to have been done.
        """
    def solve(self) -> None:
        """
        Solve the problem.

        Iterate the algorithm until the stopping criteria are satisfied.

        Note:
            Any required initializations (with init functions) are
            assumed to have been done.
        """
    def tol_simplex_size(self, value: float) -> DownhillSimplex:
        """
        Set tolerance of size of simplex.

        Args:
            value (float): Value.
        """
    @property
    def evaluations(self) -> int:
        """
        Number of function evaluations.

        :type: int
        """
    @property
    def iterations(self) -> int:
        """
        Number of iterations.

        :type: int
        """
    @property
    def opt_value(self) -> float:
        """
        Current optimal value.

        :type: float
        """
    @property
    def opt_variable(self) -> numpy.ndarray:
        """
        Current optimal variable.

        :type: numpy.ndarray
        """
    pass

class ObjectiveFunctionBase:
    """
    Base class of multi-variate objective functions.

    Inherit objective functions from this class and
    implement evaluate_on function.
    """

    def __init__(self) -> None: ...
    def evaluate_on(self, var: numpy.ndarray) -> None:
        """
        Evaluate this objective function on a variable.

        Args:
            var (numpy.ndarray): Variable.
        """
    @property
    def value(self) -> float:
        """
        Function value.

        :type: float
        """
    @value.setter
    def value(self, arg1: float) -> None:
        """
        Function value.
        """
    pass
