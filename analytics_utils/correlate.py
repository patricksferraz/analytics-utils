# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    correlate()
"""

import pandas as pd


def correlate(
    data_frame: pd.DataFrame, method: str = "pearson", min_periods: int = 1
) -> pd.DataFrame:
    """This function returns the correlation between the columns of a
    dataframe. This is the same corr function in pandas package.

    Parameters
    ----------
    data_frame : pd.DataFrame
        Input dataframe
    method : str, optional
        See pandas.DataFrame.corr, by default "pearson"
    min_periods : int, optional
        See pandas.DataFrame.corr, by default 1

    Returns
    -------
    pd.DataFrame
        Correlation matrix
    """
    return data_frame.corr(method, min_periods)


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
    ap.add_argument("--method", type=str, default="pearson")
    ap.add_argument("--min-periods", type=int, default=1)
    args = vars(ap.parse_args())

    # Apply
    result = correlate(
        pd.read_csv(args["dataset"]), args["method"], args["min_periods"]
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
