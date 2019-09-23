"""The :mod:`analystics_utils.regressors` module includes regression
algorithms."""

from .logistic_regression import logistic_regression
from .GeneralizedLinear import GeneralizedLinear
from .arima import arima


__all__ = ["logistic_regression", "GeneralizedLinear", "arima"]
