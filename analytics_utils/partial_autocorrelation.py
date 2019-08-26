# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def partial_autocorrelation(
        data_frame: pd.DataFrame,
        nlags: int = 40,
        method: str = "ywunbiased",
        alpha: float = None,
        headers: [str] = None,
    ) -> pd.DataFrame
"""

from statsmodels.tsa.stattools import pacf
import pandas as pd


def partial_autocorrelation(
    data_frame: pd.DataFrame,
    nlags: int = 40,
    method: str = "ywunbiased",
    alpha: float = None,
    headers: [str] = None,
) -> pd.DataFrame:
    """Partial autocorrelation estimated for 1d arrays. This is a adapted pacf
    function of statsmodels package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        nlags {int} -- largest lag for which the pacf is returned
            (default: {40}).
        method {str} -- A string in [‘yw’ or ‘ywunbiased’, ‘ywm’ or ‘ywmle’,
            ‘ols’, ‘ols-inefficient’, ‘ols-unbiased’, ‘ld’ or ‘ldunbiased’,
            ‘ldb’ or ‘ldbiased’] specifies which method for the calculations to
            use (default: {"ywunbiased"}).
        alpha {float} -- If a number is given, the confidence intervals for the
            given level are returned. For instance if alpha=.05, 95% confidence
            intervals are returned where the standard deviation is computed
            according to 1/sqrt(len(x)) (default: {None}).
        headers {[str]} -- chosen dataframe headers (default: {None}).

    Returns:
        pd.DataFrame -- A object with partial autocorrelations, nlags elements,
        including lag zero
    """

    if headers:
        data_frame = data_frame.loc[:, headers]

    return pd.DataFrame(
        {"pacf": pacf(data_frame, nlags=nlags, method=method, alpha=alpha)}
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
        "-n",
        "--nlags",
        type=int,
        default=40,
        help="""largest lag for which the pacf is returned (default: 40).""",
    )
    ap.add_argument(
        "-m",
        "--method",
        type=str,
        default="ywunbiased",
        help="""A string in [‘yw’ or ‘ywunbiased’, ‘ywm’ or ‘ywmle’,
        ‘ols’, ‘ols-inefficient’, ‘ols-unbiased’, ‘ld’ or ‘ldunbiased’, ‘ldb’
        or ‘ldbiased’] specifies which method for the calculations to use
        (default: "ywunbiased")""",
    )
    ap.add_argument(
        "-a",
        "--alpha",
        type=float,
        default=None,
        help="""If a number is given, the confidence intervals for the
        given level are returned. For instance if alpha=.05, 95 %% confidence
        intervals are returned where the standard deviation is computed
        according to 1/sqrt(len(x)).""",
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
        "-hd",
        "--headers",
        type=str,
        nargs="*",
        help="an string for the header in the dataset",
    )
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply ewm
    result = partial_autocorrelation(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        nlags=args["nlags"],
        method=args["method"],
        alpha=args["alpha"],
        headers=args["headers"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
