# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    seasonal()
"""

from statsmodels.tsa.seasonal import seasonal_decompose
from analytics_utils.lang import Lang
import pandas as pd


def seasonal(
    data_frame: pd.DataFrame,
    model: str = "additive",
    filt: [] = None,
    freq: int = None,
    two_sided: bool = True,
    extrapolate_trend: int = 0,
    lang: str = "pt",
    headers: [str] = None,
) -> pd.DataFrame:
    """Seasonal decomposition using moving averages. This is a adapted
    seasonal_decompose function of statsmodels package.

    Parameters
    ----------
    data_frame : pd.DataFrame
        input dataframe
    model : str, optional
        See statsmodels.tsa.seasonal.seasonal_decompose, by default "additive"
    filt : [type], optional
        See statsmodels.tsa.seasonal.seasonal_decompose, by default None
    freq : int, optional
        See statsmodels.tsa.seasonal.seasonal_decompose, by default None
    two_sided : bool, optional
        See statsmodels.tsa.seasonal.seasonal_decompose, by default True
    extrapolate_trend : int, optional
        See statsmodels.tsa.seasonal.seasonal_decompose, by default 0
    lang : str, optional
        output language, by default "pt"
    headers : [type], optional
        chosen dataframe headers, by default None

    Returns
    -------
    pd.DataFrame
        A object with observed, seasonal, trend, and resid attributes
    """

    lang = Lang(lang)

    if headers:
        data_frame = data_frame.loc[:, headers]

    seasonal = seasonal_decompose(
        data_frame,
        model=model,
        filt=filt,
        freq=freq,
        two_sided=two_sided,
        extrapolate_trend=extrapolate_trend,
    )
    return pd.DataFrame(
        [
            {
                lang.word("observed"): seasonal.observed,
                lang.word("seasonal"): seasonal.seasonal,
                lang.word("trend"): seasonal.trend,
                lang.word("resid"): seasonal.resid,
            }
        ]
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
        "-l",
        "--lang",
        type=str,
        default="pt",
        help="language for the output result {'pt', 'en'} (default: 'pt')",
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
    ap.add_argument("--model", type=str, default="additive")
    ap.add_argument("--filt", nargs="*")
    ap.add_argument("--freq", type=int, default=None)
    ap.add_argument("--two-sided", type=bool, default=True)
    ap.add_argument("--extrapolate-trend", type=int, default=0)
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply
    result = seasonal(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        model=args["model"],
        filt=args["filt"],
        freq=args["freq"],
        two_sided=args["two_sided"],
        extrapolate_trend=args["extrapolate_trend"],
        lang=args["lang"],
        headers=args["headers"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
