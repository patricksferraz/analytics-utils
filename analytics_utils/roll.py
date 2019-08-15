# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def roll(
        data_frame: pd.DataFrame,
        window: int,
        roll_type: str = "mean",
        headers: [str] = None,
    ) -> pd.DataFrame
"""

import pandas as pd


def roll(
    data_frame: pd.DataFrame,
    window: int,
    roll_type: str = "mean",
    headers: [str] = None,
) -> pd.DataFrame:
    """This function Provide rolling window calculations. This is a adapted
    rolling function of pandas package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        window {int} -- Size of the moving window. This is the number of
        observations used for calculating the statistic. Each window will be a
        fixed size.
        roll_type {str} -- {‘mean’, ‘var’, 'std'} (default: {"mean"}).
        headers {[str]} -- chosen dataframe headers (default: {None}).

    Returns:
        pd.DataFrame -- a Window or Rolling sub-classed for the particular
        operation.
    """
    rolling = {
        "mean": lambda roll: roll.mean(),
        "var": lambda roll: roll.var(),
        "std": lambda roll: roll.std(),
    }

    if headers:
        data_frame = data_frame.loc[:, headers]
    return rolling[roll_type](data_frame.rolling(window))


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
        "-w",
        "--window",
        type=int,
        required=True,
        help="""Size of the moving window. This is the number of
        observations used for calculating the statistic. Each window will be a
        fixed size.""",
    )
    ap.add_argument(
        "-t",
        "--roll_type",
        type=str,
        default="mean",
        help="""{‘mean’, ‘var’, 'std'} (default: {"mean"}).""",
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

    # Generates the data description
    result = roll(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        window=args["window"],
        roll_type=args["roll_type"],
        headers=args["headers"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
