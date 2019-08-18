# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def linear_regression(
        data_frame: pd.DataFrame,
        fit_intercept: bool = True,
        normalize: bool = False,
        copy_X: bool = True,
        n_jobs: int = None,
        offset: int = 1,
        regressors: [str] = None,
        predictors: [str] = None,
    ) -> pd.DataFrame
"""

from sklearn.linear_model import LinearRegression
import pandas as pd


def linear_regression(
    data_frame: pd.DataFrame,
    fit_intercept: bool = True,
    normalize: bool = False,
    copy_X: bool = True,
    n_jobs: int = None,
    offset: int = 1,
    regressors: [str] = None,
    predictors: [str] = None,
) -> pd.DataFrame:
    """Ordinary least squares Linear Regression. This is a adapted
    LinearRegression function of scikit-learn package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        fit_intercept {bool} -- whether to calculate the intercept for this
        model. If set to False, no intercept will be used in calculations (e.g.
        data is expected to be already centered) (default: {True})
        normalize {bool} -- This parameter is ignored when fit_intercept is set
        to False. If True, the regressors X will be normalized before
        regression by subtracting the mean and dividing by the l2-norm
        (default: {False})
        copy_X {bool} -- If True, X will be copied; else, it may be overwritten
        (default: {True})
        n_jobs {int} -- The number of jobs to use for the computation. This
        will only provide speedup for n_targets > 1 and sufficient large
        problems (default: {None})
        offset {int} -- Offset for predict (p.ex. if 1 regressor [:-1]
        predictor [1:]) (default: {1})
        regressors {[str]} -- chosen dataframe headers for regressor
        (default: {None}).
        predictors {[str]} -- chosen dataframe headers for predcitor
        (default: {None}).

    Raises:
        ValueError: Offset cannot be less than 1
        ValueError: Predictors cannot be None

    Returns:
        pd.DataFrame -- Returns predicted values.
    """

    if offset < 1:
        raise ValueError("Offset cannot be less than 1")
    if not predictors:
        raise ValueError("Predictors cannot be None")
    y = data_frame[offset:].loc[:, predictors]

    if regressors:
        data_frame = data_frame.loc[:, regressors]
    x = data_frame[:-offset]

    model = LinearRegression().fit(x, y)

    return pd.DataFrame(
        model.predict(data_frame), columns=["predict_" + p for p in predictors]
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
        "-fi",
        "--fit-intercept",
        type=bool,
        default=True,
        help="""whether to calculate the intercept for this model. If set to
        False, no intercept will be used in calculations (e.g. data is expected
        to be already centered) (default: True).""",
    )
    ap.add_argument(
        "-n",
        "--normalize",
        type=bool,
        default=False,
        help="""This parameter is ignored when fit_intercept is set to False.
        If True, the regressors X will be normalized before regression by
        subtracting the mean and dividing by the l2-norm (default: False)""",
    )
    ap.add_argument(
        "-c",
        "--copy-X",
        type=bool,
        default=True,
        help="""If True, X will be copied; else, it may be overwritten
        (default: True).""",
    )
    ap.add_argument(
        "-nj",
        "--n-jobs",
        type=int,
        default=None,
        help="""The number of jobs to use for the computation. This will only
        provide speedup for n_targets > 1 and sufficient large problems
        (default: None).""",
    )
    ap.add_argument(
        "-off",
        "--offset",
        type=int,
        default=1,
        help="""Offset for predict (p.ex. if 1 regressor [:-1] predictor [1:])
        (default: 1).""",
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
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply ewm
    result = linear_regression(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        fit_intercept=args["fit_intercept"],
        normalize=args["normalize"],
        copy_X=args["copy_X"],
        n_jobs=args["n_jobs"],
        offset=args["offset"],
        regressors=args["regressors"],
        predictors=args["predictors"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
