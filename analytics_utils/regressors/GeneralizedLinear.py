# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    linear_regression()
"""

from sklearn.linear_model import MultiTaskElasticNetCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
import pandas as pd
import numpy as np


class GeneralizedLinear:
    _LINEAR_TYPES_CV = {
        "MultiTaskElasticNetCV": MultiTaskElasticNetCV,
        "ElasticNetCV": ElasticNetCV,
        "RidgeCV": RidgeCV,
        "LassoCV": LassoCV,
    }
    LINEAR_TYPES = {"LinearRegression": LinearRegression, **_LINEAR_TYPES_CV}

    def __init__(
        self,
        df_true: pd.DataFrame,
        df_pred: pd.DataFrame = None,
        fit_intercept: bool = True,
        normalize: bool = False,
        time_step: int = 1,
        linear_type: str = "LinearRegression",
        cv: int = 5,
        alphas: [float] = None,
        regressors: [str] = None,
        predictors: [str] = None,
    ):
        """GeneralizedLinear. This is a adapted Linear functions of
        scikit-learn package.

        Arguments:
            df_true {pd.DataFrame} -- input dataframe for 'train'

        Keyword Arguments:
            df_pred {pd.DataFrame} -- input dataframe for forecasting
                (default: {None})
            time_step {int} -- time_step for predict (p.ex. if 1 forecasting
                for next 1 time_step) (default: {1})
            linear_type {str} -- Linear type for apply.
                {'MultiTaskElasticNetCV', 'ElasticNetCV', 'RidgeCV', 'LassoCV',
                'LinearRegression'} (default: {"LinearRegression"})
            regressors {[type]} -- chosen dataframe headers for regressor
                (default: {None})
            predictors {[type]} -- chosen dataframe headers for predcitor
                (default: {None})

            {others params} -- See sklearn.linear_model...
        """
        self.df_true = df_true.copy()
        self.df_pred = df_pred.copy() if df_pred else self.df_true
        self.fit_intercept = fit_intercept
        self.normalize = normalize
        self.time_step = time_step
        self.linear_type = linear_type
        self.cv = cv
        self.alphas = alphas
        self.regressors = regressors
        self.predictors = predictors
        self.models = {}

        if self.regressors is not None:
            self.df_true = self.df_true[regressors]
            self.df_pred = self.df_pred[regressors]

        if self.linear_type in self._LINEAR_TYPES_CV and self.alphas is None:
            self.alphas = 10 ** np.linspace(
                start=-2, stop=1, num=20, dtype=float
            )

        self._validate()

    def _validate(self):
        """Validate class params

        Raises:
            ValueError: time_step cannot be less than 1
            ValueError: Predictors cannot be None
            ValueError: linear_type {linear_type} not exists
        """
        if self.time_step < 1:
            raise ValueError("time_step cannot be less than 1")
        if self.predictors is None:
            raise ValueError("Predictors cannot be None")
        if self.linear_type not in self.LINEAR_TYPES:
            raise ValueError(f"linear_type {self.linear_type} not exists")

    def fit(self):
        """Fit from linear_type defined
        """
        for ts in range(1, self.time_step + 1):
            # Get predictors
            y_true = self.df_true[self.predictors][ts:]
            x_true = self.df_true[:-ts]

            # Params
            params = {
                "fit_intercept": self.fit_intercept,
                "normalize": self.normalize,
            }

            # Adds alphas for CV
            if self.linear_type in self._LINEAR_TYPES_CV:
                params["alphas"] = self.alphas
                params["cv"] = self.cv

            # Fit model
            self.models[ts] = self.LINEAR_TYPES[self.linear_type](
                **params
            ).fit(x_true, y_true)

    def forecasting(self):
        """Forecasting from linear_type defined
        """
        for _ in self.models:
            yield self.models[_].predict(
                self.df_true if self.df_pred is None else self.df_pred
            )

    def run(self):
        """Exec fit and forecasting from linear_type defined

        Returns:
            pd.DataFrame -- Forecasting from linear_type using time_step size
        """
        self.fit()
        return pd.concat(
            [pd.DataFrame(_) for _ in self.forecasting()],
            ignore_index=True,
            axis=1,
        )


if __name__ == "__main__":
    import argparse

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-d", "--dataset", required=True, help="path to input dataset"
    )
    ap.add_argument(
        "-f", "--file-out", type=str, help="path to file of output json"
    )
    ap.add_argument(
        "-o",
        "--orient",
        type=str,
        default="columns",
        help="""format json output
        {'split', 'records', 'index', 'values', 'table', 'columns'}
        (default: 'columns')""",
    )
    ap.add_argument(
        "-ts",
        "--time-step",
        type=int,
        default=1,
        help="""time_step for predict (p.ex. if 1 forecasting for next 1
        time_step) (default: 1).""",
    )
    ap.add_argument(
        "-lt",
        "--linear-type",
        type=int,
        default=1,
        help="""Linear type for apply. {'MultiTaskElasticNetCV',
        'ElasticNetCV', 'RidgeCV', 'LassoCV', 'LinearRegression'}
        (default: 'LinearRegression').""",
    )
    ap.add_argument(
        "-pd",
        "--parse-dates",
        type=str,
        nargs="*",
        help="""Headers of columns to parse dates. A column named datetime is
        created.""",
    )
    ap.add_argument(
        "-i",
        "--index",
        type=str,
        nargs="*",
        help="Headers of columns to set as index.",
    )
    ap.add_argument(
        "-r",
        "--regressors",
        type=str,
        nargs="*",
        help="an string for the header (regressors) in the dataset",
    )
    ap.add_argument(
        "-p",
        "--predictors",
        type=str,
        nargs="+",
        help="an string for the header (predictors) in the dataset",
    )
    ap.add_argument("--fit-intercept", type=bool, default=True)
    ap.add_argument("--normalize", type=bool, default=False)
    ap.add_argument("--alphas", type=float, nargs="*")
    ap.add_argument("--cv", type=int, default=5)
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply ewm
    result = GeneralizedLinear(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        fit_intercept=args["fit_intercept"],
        normalize=args["normalize"],
        time_step=args["time_step"],
        linear_type=args["linear_type"],
        cv=args["cv"],
        alphas=args["alphas"],
        regressors=args["regressors"],
        predictors=args["predictors"],
    ).run()

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
