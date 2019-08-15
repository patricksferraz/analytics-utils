# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def ewm(
        data_frame: pd.DataFrame,
        com: float = None,
        span: float = None,
        halflife: float = None,
        alpha: float = None,
        ignore_na: bool = False,
        ewm_type: str = "mean",
        headers: [str] = None,
    ) -> pd.DataFrame
"""

import pandas as pd


def ewm(
    data_frame: pd.DataFrame,
    com: float = None,
    span: float = None,
    halflife: float = None,
    alpha: float = None,
    ignore_na: bool = False,
    ewm_type: str = "mean",
    headers: [str] = None,
) -> pd.DataFrame:
    """This function provide exponential weighted functions. This is a adapted
    ewm function of pandas package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        com {int} -- Specify decay in terms of center of mass, α=1/(1+com),
        for com≥0 (default: {None}).
        span {float} -- Specify decay in terms of span, α=2/(span+1),
        for span≥1. (default: {None}).
        halflife {float} -- Specify decay in terms of half-life,
        α=1−exp(log(0.5)/halflife),for halflife>0 (default: {None}).
        alpha {float} -- Specify smoothing factor α directly, 0<α≤1
        (default: {None}).
        ignore_na {bool} -- Ignore missing values when calculating weights;
        specify True to reproduce pre-0.15.0 behavior.(default: {False}).
        ewm_type {str} -- {‘mean’, ‘var’, 'std'} (default: {"mean"}).
        headers {[str]} -- chosen dataframe headers (default: {None}).

    Returns:
        pd.DataFrame -- A Window sub-classed for the particular operation.
    """
    ewm = {
        "mean": lambda ewm: ewm.mean(),
        "var": lambda ewm: ewm.var(),
        "std": lambda ewm: ewm.std(),
    }

    if headers:
        data_frame = data_frame.loc[:, headers]
    return ewm[ewm_type](
        data_frame.ewm(
            com=com,
            span=span,
            halflife=halflife,
            alpha=alpha,
            ignore_na=ignore_na,
        )
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
        help=""""format json output
        {'split', 'records', 'index', 'values', 'table', 'columns'}
        (default: 'columns')""",
    )
    ap.add_argument(
        "-c",
        "--com",
        type=float,
        default=None,
        help="""Specify decay in terms of center of mass,
        α=1/(1+com), for com≥0 (default: None).""",
    )
    ap.add_argument(
        "-s",
        "--span",
        type=float,
        default=None,
        help="""Specify decay in terms of span, α=2/(span+1), for span≥1.
        (default: None).""",
    )
    ap.add_argument(
        "-hl",
        "--halflife",
        type=float,
        default=None,
        help="""Specify decay in terms of half-life, α=1−exp(log(0.5)/halflife)
        , for halflife>0 (default: None).""",
    )
    ap.add_argument(
        "-a",
        "--alpha",
        type=float,
        default=None,
        help="""Specify smoothing factor α directly, 0<α≤1 (default: None).""",
    )
    ap.add_argument(
        "-ina",
        "--ignore-na",
        type=bool,
        default=False,
        help="""Ignore missing values when calculating weights; specify
        True to reproduce (default: False).""",
    )
    ap.add_argument(
        "-t",
        "--ewm-type",
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

    # Apply ewm
    result = ewm(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        com=args["com"],
        span=args["span"],
        halflife=args["halflife"],
        alpha=args["alpha"],
        ignore_na=args["ignore_na"],
        ewm_type=args["ewm_type"],
        headers=args["headers"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
