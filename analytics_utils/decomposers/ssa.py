# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def ssa(
        data_frame: pd.DataFrame,
        window_size: int or float = 4,
        groups: int or [int] = None,
        headers: [str] = None,
    ) -> pd.DataFrame
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
        window_size {int or float} -- Size of the sliding window (i.e. the size
        of each word). If float, it represents the percentage of the size of
        each time series and must be between 0 and 1. The window size will be
        computed as ``max(2, ceil(self.window_size * n_timestamps))``
        (default: {4}).
        groups {int or [int]} -- The way the elementary matrices are grouped. If
        None, no grouping is performed. If an integer, it represents the number
        of groups and the bounds of the groups are computed as
        ``np.linspace(0, window_size, groups + 1).astype('int64')``.
        If array-like, each element must be array-like and contain the indices
        for each group. (default: {None}).
        headers {[str]} -- chosen dataframe headers (default: {None}).

    Returns:
        pd.DataFrame -- A object decomposed of length window_size for each
        feature (header).
    """

    # changes columns to index
    data_frame = data_frame.T
    if headers:
        data_frame = data_frame.loc[headers]

    # Generates window_size (default:4) lists for each feature
    ssa = SingularSpectrumAnalysis(window_size, groups)
    x_ssa = ssa.fit_transform(data_frame)

    # Decompose each feature adding each window_size in line
    decompose = {}
    if len(headers) > 1:
        for idx, h in enumerate(headers):
            decompose[h] = [x for x in x_ssa[idx]]
    else:
        decompose[headers[0]] = [x for x in x_ssa]

    return pd.DataFrame(decompose)


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
        "--window-size",
        type=int or float,
        default=2,
        help="""Size of the sliding window (i.e. the size of each
        word). If float, it represents the percentage of the size of each time
        series and must be between 0 and 1. The window size will be computed as
        ``max(2, ceil(self.window_size * n_timestamps))`` (default: 4}).""",
    )
    ap.add_argument(
        "-g",
        "--groups",
        type=int,
        nargs="*",
        help="""The way the elementary matrices are grouped. If
        None, no grouping is performed. If an integer, it represents the number
        of groups and the bounds of the groups are computed as
        ``np.linspace(0, window_size, groups + 1).astype('int64')``.
        If array-like, each element must be array-like and contain the indices
        for each group. (default: None).""",
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
