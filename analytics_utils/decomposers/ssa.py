# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    ssa()
"""

from pyts.decomposition import SingularSpectrumAnalysis
import pandas as pd


def ssa(
    data_frame: pd.DataFrame,
    window_size: int or float = 4,
    groups: int or [int] = None,
    headers: [str] = None,
) -> pd.DataFrame:
    """Singular Spectrum Analysis. This is a adapted SingularSpectrumAnalysis
    function of pyts package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        headers {[str]} -- chosen dataframe headers (default: {None}).

        {others params} -- See pyts.decomposition.SingularSpectrumAnalysis

    Returns:
        pd.DataFrame -- A object decomposed of length window_size for each
        feature (header).
    """

    # Select and changes columns to index
    if headers is None:
        headers = data_frame.columns
    else:
        data_frame = data_frame[headers]

    # Generates window_size (default:4) lists for each feature
    ssa = SingularSpectrumAnalysis(window_size, groups)
    x_ssa = ssa.fit_transform(data_frame.T)

    # Decompose each feature adding each window_size in line
    decompose = [[x for x in x_ssa[i]] for i, _ in enumerate(headers)]

    return pd.DataFrame(decompose, index=headers).T


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
        type=str,
        nargs="*",
        help="an string for the header in the dataset",
    )
    ap.add_argument("--window-size", type=int or float, default=4)
    ap.add_argument("--groups", type=int, nargs="*")
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply ssa
    result = ssa(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        window_size=args["window_size"],
        groups=args["groups"],
        headers=args["headers"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
