# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    describe_data()
"""

from analytics_utils.lang import Lang
import pandas as pd


FIRST_QUARTILE = 0.25
THIRD_QUARTILE = 0.75
IQR_CONSTANT = 1.5


def describe_data(
    data_frame: pd.DataFrame, lang: str = "pt", headers: [str] = None
) -> pd.DataFrame:
    """This function describe the datas of a dataframe. Returning the max,
    min, mean, median, quantile, variance, standard deviation,
    mean absolute deviation, amplitude, root mean squared, kurtosis, skewness
    and count for all headers in dataframe

    Parameters
    ----------
    data_frame : pd.DataFrame
        Dataframe of input
    lang : str, optional
        Output language, by default "pt"
    headers : [str], optional
        Chosen dataframe headers, by default None

    Returns
    -------
    pd.DataFrame
        Dataframe with the descriptions
    """

    lang = Lang(lang)

    def _apply(header: str, column: []):
        _max = column.max()
        _min = column.min()

        # Scatter
        _q1 = column.quantile(FIRST_QUARTILE)
        _q3 = column.quantile(THIRD_QUARTILE)
        _iqr = _q3 - _q1
        _lower = max(_min, _q1 - (IQR_CONSTANT * _iqr))
        _upper = min(_max, _q3 + (IQR_CONSTANT * _iqr))

        return {
            lang.word("header"): header,
            lang.word("max"): _max,
            lang.word("min"): _min,
            lang.word("mean"): column.mean(),
            lang.word("median"): column.median(),
            lang.phrase("limit", lang.word("lower")): _lower,
            lang.phrase("quartile", "1"): _q1,
            lang.phrase("quartile", "3"): _q3,
            lang.phrase("limit", lang.word("upper")): _upper,
            lang.word("var"): column.var(),
            lang.word("std"): column.std(),
            lang.word("mad"): column.mad(),
            lang.word("amp"): _max - _min,
            lang.word("rms"): (column.pow(2)).mean() ** 0.5,
            lang.word("kurtosis"): column.kurtosis(),
            lang.word("skew"): column.skew(),
            lang.word("count"): column.count(),
            lang.word("nans"): column.isna().sum(),
        }

    if not headers:
        headers = data_frame.columns

    return pd.DataFrame(
        [_apply(_, data_frame.loc[:, _]) for _ in headers]
    ).set_index(lang.word("header"))


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
        metavar="H",
        type=str,
        nargs="*",
        help="an string for the header in the dataset",
    )
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply
    result = describe_data(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        lang=args["lang"],
        headers=args["headers"],
    )
    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
