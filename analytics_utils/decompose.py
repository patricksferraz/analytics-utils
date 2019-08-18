# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    def decompose(
        data_frame: pd.DataFrame,
        model: str = "additive",
        filt: [] = None,
        freq: int = None,
        two_sided: bool = True,
        extrapolate_trend: int = 0,
        lang: str = "pt",
        headers: [str] = None,
    ) -> pd.DataFrame
"""

from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd

if __name__ == "__main__":
    from lang.words import words
else:
    from analytics_utils.lang.words import words


def decompose(
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

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        model {str} -- {“additive”, “multiplicative”}. Type of seasonal
        component. Abbreviations are accepted (default: {'additive'}).
        filt {[]]} -- The filter coefficients for filtering out the seasonal
        component. The concrete moving average method used in filtering is
        determined by two_sided.(default: {None}).
        freq {int} -- Frequency of the series. Must be used if x is not a
        pandas object. Overrides default periodicity of x if x is a pandas
        object with a timeseries index (default: {None}).
        two_sided {bool} -- The moving average method used in filtering. If
        True, a centered moving average is computed using the filt.
        If False, the filter coefficients are for past values only
        (default: {True}).
        extrapolate_trend {int} -- If set to > 0, the trend resulting from the
        convolution is linear least-squares extrapolated on both ends (or the
        single one if two_sided is False) considering this many (+1) closest
        points. If set to ‘freq’, use freq closest points. Setting this
        parameter results in no NaN values in trend or resid components
        (default: {0}).
        lang {str} -- output language (default: {"pt"}).
        headers {[str]} -- chosen dataframe headers (default: {None}).

    Returns:
        pd.DataFrame -- A object with observed, seasonal, trend, and resid
        attributes.
    """

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
                words["observed"][lang]: seasonal.observed,
                words["seasonal"][lang]: seasonal.seasonal,
                words["trend"][lang]: seasonal.trend,
                words["resid"][lang]: seasonal.resid,
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
        "-m",
        "--model",
        type=str,
        default="additive",
        help="""Type of seasonal component. Abbreviations are accepted
        {“additive”, “multiplicative”} (default: 'additive').""",
    )
    ap.add_argument(
        "-ft",
        "--filt",
        nargs="*",
        help="""The filter coefficients for filtering out the seasonal
        component. The concrete moving average method used in filtering is
        determined by two_sided (default: None).""",
    )
    ap.add_argument(
        "-fq",
        "--freq",
        type=int,
        default=None,
        help="""Frequency of the series. Must be used if x is not a
        pandas object. Overrides default periodicity of x if x is a pandas
        object with a timeseries index (default: None).""",
    )
    ap.add_argument(
        "-t",
        "--two-sided",
        type=bool,
        default=True,
        help="""The moving average method used in filtering. If
        True (default), a centered moving average is computed using the filt.
        If False, the filter coefficients are for past values only
        (default: True).""",
    )
    ap.add_argument(
        "-e",
        "--extrapolate-trend",
        type=int,
        default=0,
        help="""If set to > 0, the trend resulting from the
        convolution is linear least-squares extrapolated on both ends (or the
        single one if two_sided is False) considering this many (+1) closest
        points. If set to ‘freq’, use freq closest points. Setting this
        parameter results in no NaN values in trend or resid components
        (default: 0).""",
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
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply ewm
    result = decompose(
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
