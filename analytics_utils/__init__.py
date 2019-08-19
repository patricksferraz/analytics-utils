"""The :mod:`analystics_utils` module includes analytics algorithms."""

from .partial_autocorrelation import partial_autocorrelation
from .linear_regression import linear_regression
from .autocorrelation import autocorrelation
from .describe_data import describe_data
from .interpolate import interpolate
from .correlate import correlate
from .roll import roll
from .ewm import ewm

__all__ = [
    "partial_autocorrelation",
    "linear_regression",
    "autocorrelation",
    "describe_data",
    "interpolate",
    "correlate",
    "roll",
    "ewm",
]
