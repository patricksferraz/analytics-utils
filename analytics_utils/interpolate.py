# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def interpolate(
        data_frame: pd.DataFrame,
        headers: [str] = None,
        method: str = "linear",
        limit: int = None,
    ) -> pd.DataFrame
"""

import pandas as pd


def interpolate(
    data_frame: pd.DataFrame,
    limit: int = None,
    method: str = "linear",
    headers: [str] = None,
) -> pd.DataFrame:
    """This function returns the Series or DataFrame of same shape interpolated
    at the NaNs. This is a adapted interpolate function of pandas package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        limit {int} -- Maximum number of consecutive NaNs to fill
        (default: {None}).
        method {str} -- {‘linear’, ‘time’, ‘index’, ‘values’, ‘nearest’,
        ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘barycentric’, ‘krogh’,
        ‘polynomial’, ‘spline’ ‘piecewise_polynomial’, ‘pchip’}
        (default: {"linear"}).
        headers {[str]} -- chosen dataframe headers (default: {None}).

    Returns:
        pd.DataFrame -- Series or DataFrame of same shape interpolated at the
        NaNs
    """
    if headers:
        data_frame = data_frame.loc[:, headers]
    return data_frame.interpolate(method, limit=limit)


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
        "-m",
        "--method",
        type=str,
        default="linear",
        help="""method of interpolation {‘linear’, ‘time’, ‘index’, ‘values’,
        ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘barycentric’,
        ‘krogh’, ‘polynomial’, ‘spline’ ‘piecewise_polynomial’, ‘pchip’}
        (default: 'linear')""",
    )
    ap.add_argument(
        "-l",
        "--limit",
        type=int,
        default=None,
        help="""Maximum number of consecutive NaNs to fill (default: None)""",
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
        metavar="H",
        type=str,
        nargs="*",
        help="an string for the header in the dataset",
    )
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Interpolated datas
    result = interpolate(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        limit=args["limit"],
        method=args["method"],
        headers=args["headers"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
