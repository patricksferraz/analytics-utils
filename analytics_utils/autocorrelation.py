# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def autocorrelation(
        data_frame: pd.DataFrame,
        unbiased: bool = False,
        nlags: int = 40,
        fft: bool = None,
        alpha: float = None,
        missing: str = "none",
        lang: str = "pt",
        headers: [str] = None,
    ) -> pd.DataFrame
"""

from statsmodels.tsa.stattools import acf
import pandas as pd


def autocorrelation(
    data_frame: pd.DataFrame,
    unbiased: bool = False,
    nlags: int = 40,
    fft: bool = None,
    alpha: float = None,
    missing: str = "none",
    headers: [str] = None,
) -> pd.DataFrame:
    """Autocorrelation function for 1d arrays. This is a adapted acf function
    of statsmodels package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        unbiased {bool} -- If True, then denominators for autocovariance are
        n-k, otherwise n (default: {False}).
        nlags {int} --     Number of lags to return autocorrelation for
        (default: {40}).
        fft {bool} -- If True, computes the ACF via FFT (default: {None}).
        alpha {float} -- If a number is given, the confidence intervals for the
        given level are returned. For instance if alpha=.05, 95 % confidence
        intervals are returned where the standard deviation is computed
        according to Bartlett’s formula (default: {None}).
        missing {str} -- A string in [‘none’, ‘raise’, ‘conservative’, ‘drop’]
        specifying how the NaNs are to be treated (default: {"none"}).
        headers {[str]} -- chosen dataframe headers (default: {None}).

    Returns:
        pd.DataFrame -- A object with autocorrelation function.
    """

    if headers:
        data_frame = data_frame.loc[:, headers]

    return pd.DataFrame(
        {
            "acf": acf(
                data_frame,
                unbiased=unbiased,
                nlags=nlags,
                fft=fft,
                alpha=alpha,
                missing=missing,
            )
        }
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
        "-u",
        "--unbiased",
        type=bool,
        default=False,
        help="""If True, then denominators for autocovariance are n-k,
        otherwise n""",
    )
    ap.add_argument(
        "-n",
        "--nlags",
        type=int,
        default=40,
        help="""Number of lags to return autocorrelation for (default: 40).""",
    )
    ap.add_argument(
        "-fft",
        "--fft",
        type=bool,
        default=None,
        help="""If True, computes the ACF via FFT.""",
    )
    ap.add_argument(
        "-a",
        "--alpha",
        type=float,
        default=None,
        help="""If a number is given, the confidence intervals for the given
        level are returned. For instance if alpha=.05, 95 %% confidence
        intervals are returned where the standard deviation is computed
        according to Bartlett’s formula.""",
    )
    ap.add_argument(
        "-m",
        "--missing",
        type=str,
        default="none",
        help="""A string in [‘none’, ‘raise’, ‘conservative’, ‘drop’]
        specifying how the NaNs are to be treated.""",
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
    result = autocorrelation(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        unbiased=args["unbiased"],
        nlags=args["nlags"],
        fft=args["fft"],
        alpha=args["alpha"],
        missing=args["missing"],
        headers=args["headers"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
