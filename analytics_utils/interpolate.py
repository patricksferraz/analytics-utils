# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    interpolate()
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

    Parameters
    ----------
    data_frame : pd.DataFrame
        input dataframe
    limit : int, optional
        See pandas.DataFrame.interpolate, by default None
    method : str, optional
        See pandas.DataFrame.interpolate, by default "linear"
    headers : [str], optional
        chosen dataframe headers, by default None

    Returns
    -------
    pd.DataFrame
        Series or DataFrame of same shape interpolated at the NaNs
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
    ap.add_argument("--method", type=str, default="linear")
    ap.add_argument("--limit", type=int, default=None)
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply
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
