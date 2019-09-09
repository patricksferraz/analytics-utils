"""The :mod:`analystics_utils.regressors` module includes regression
algorithms."""

from .logistic_regression import logistic_regression
from .linear_regression import linear_regression


__all__ = ["logistic_regression", "linear_regression"]
