# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    autocorrelation()
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

    Parameters
    ----------
    data_frame : pd.DataFrame
        Input dataframe
    unbiased : bool, optional
        See statsmodels.tsa.stattools.acf, by default False
    nlags : int, optional
        See statsmodels.tsa.stattools.acf, by default 40
    fft : bool, optional
        See statsmodels.tsa.stattools.acf, by default None
    alpha : float, optional
        See statsmodels.tsa.stattools.acf, by default None
    missing : str, optional
        See statsmodels.tsa.stattools.acf, by default "none"
    headers : [type], optional
        Chosen dataframe headers, by default None

    Returns
    -------
    pd.DataFrame
        A object with autocorrelation function.
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
    ap.add_argument("--unbiased", type=bool, default=False)
    ap.add_argument("--nlags", type=int, default=40)
    ap.add_argument("--fft", type=bool, default=None)
    ap.add_argument("--alpha", type=float, default=None)
    ap.add_argument("--missing", type=str, default="none")
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply
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
