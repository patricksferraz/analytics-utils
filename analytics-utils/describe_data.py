# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    describe_data(data_frame: pd.DataFrame, headers: [str], lang: str = "pt")
"""

from lang.words import words
from lang.phrases import phrases
import pandas as pd


def describe_data(
    data_frame: pd.DataFrame, headers: [str], lang: str = "pt"
) -> pd.DataFrame:
    """This function describe the datas of a dataframe. Returning the max,
    min, mean, median, quantile, variance, standard deviation,
    mean absolute deviation, amplitude, root mean squared, kurtosis, skewness
    and count for all headers in dataframe

    Arguments:
        data_frame {pd.DataFrame} -- dataframe of input
        headers {[type]} -- chosen dataframe headers

    Keyword Arguments:
        lang {str} -- output language (default: {"pt"})

    Returns:
        pd.Dataframe -- dataframe with the descriptions
    """

    def _apply(header: str, column: []):
        try:
            _max = column.max()
            _min = column.min()
            _count = column.count()

            return {
                words["header"][lang]: header,
                words["max"][lang]: _max,
                words["min"][lang]: _min,
                words["mean"][lang]: column.mean(),
                words["median"][lang]: column.median(),
                words["quantile"][lang]("1"): column.quantile(),
                words["var"][lang]: column.var(),
                words["std"][lang]: column.std(),
                words["mad"][lang]: column.mad(),
                words["amp"][lang]: _max - _min,
                words["rms"][lang]: sum((column.pow(2)) / (_count)) ** (1 / 2),
                words["kurtosis"][lang]: column.kurtosis(),
                words["skew"][lang]: column.skew(),
                words["count"][lang]: _count,
            }
        except KeyError:
            return {"error": phrases["unsupported"]["pt"](words["lang"]["pt"])}

    return pd.DataFrame([_apply(_, data_frame.loc[:, _]) for _ in headers])


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
        "-l",
        "--lang",
        type=str,
        default="pt",
        help="language for the output result (pt|en)",
    )
    ap.add_argument(
        "-o",
        "--orient",
        type=str,
        default="columns",
        help="format json output (split|records|index|values|table|columns)",
    )
    ap.add_argument(
        "header",
        metavar="H",
        type=str,
        nargs="+",
        help="an string for the header in the dataset",
    )
    args = vars(ap.parse_args())

    # Generates the data description
    result = describe_data(
        pd.read_csv(args["dataset"]), args["header"], args["lang"]
    )
    # Output in json format
    print(result.to_json(args.get("file-out"), orient=args["orient"]))
