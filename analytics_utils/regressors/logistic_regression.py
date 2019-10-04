# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    logistic_regression()
"""

from sklearn.linear_model import LogisticRegression
import pandas as pd


def logistic_regression(
    data_frame: pd.DataFrame,
    penalty: str = "l2",
    dual: bool = False,
    tol: float = 1e-4,
    C: float = 1.0,
    fit_intercept: bool = True,
    intercept_scaling: float = 1,
    class_weight: dict or str = None,
    random_state: int or str = None,
    solver: str = "liblinear",
    max_iter: int = 100,
    multi_class: str = "ovr",
    verbose: int = 0,
    warm_start: bool = False,
    n_jobs: int = None,
    l1_ratio: float = None,
    offset: int = 1,
    regressors: [str] = None,
    predictors: [str] = None,
) -> pd.DataFrame:
    """Logistic Regression (aka logit, MaxEnt) classifier. This is a adapted
    LogisticRegression function of scikit-learn package.

    Parameters
    ----------
    data_frame : pd.DataFrame
        input dataframe
    penalty : str, optional
        See sklearn.linear_model.LogisticRegression, by default "l2"
    dual : bool, optional
        See sklearn.linear_model.LogisticRegression, by default False
    tol : float, optional
        See sklearn.linear_model.LogisticRegression, by default 1e-4
    C : float, optional
        See sklearn.linear_model.LogisticRegression, by default 1.0
    fit_intercept : bool, optional
        See sklearn.linear_model.LogisticRegression, by default True
    intercept_scaling : float, optional
        See sklearn.linear_model.LogisticRegression, by default 1
    class_weight : dictorstr, optional
        See sklearn.linear_model.LogisticRegression, by default None
    random_state : intorstr, optional
        See sklearn.linear_model.LogisticRegression, by default None
    solver : str, optional
        See sklearn.linear_model.LogisticRegression, by default "liblinear"
    max_iter : int, optional
        See sklearn.linear_model.LogisticRegression, by default 100
    multi_class : str, optional
        See sklearn.linear_model.LogisticRegression, by default "ovr"
    verbose : int, optional
        See sklearn.linear_model.LogisticRegression, by default 0
    warm_start : bool, optional
        See sklearn.linear_model.LogisticRegression, by default False
    n_jobs : int, optional
        See sklearn.linear_model.LogisticRegression, by default None
    l1_ratio : float, optional
        See sklearn.linear_model.LogisticRegression, by default None
    offset : int, optional
        Offset for predict (p.ex. if 1 regressor [:-1] predictor [1:]), by
        default 1
    regressors : [str], optional
        chosen dataframe headers for regressor, by default None
    predictors : [str], optional
        chosen dataframe headers for predcitor, by default None

    Returns
    -------
    pd.DataFrame
        Returns predicted values

    Raises
    ------
    ValueError
        Offset cannot be less than 1
    ValueError
        Predictors cannot be None
    """
    if offset < 1:
        raise ValueError("Offset cannot be less than 1")
    if not predictors:
        raise ValueError("Predictors cannot be None")
    y = data_frame[offset:].loc[:, predictors]

    if regressors:
        data_frame = data_frame.loc[:, regressors]
    x = data_frame[:-offset]

    model = LogisticRegression(
        penalty=penalty,
        dual=dual,
        tol=tol,
        C=C,
        fit_intercept=fit_intercept,
        intercept_scaling=intercept_scaling,
        class_weight=class_weight,
        random_state=random_state,
        solver=solver,
        max_iter=max_iter,
        multi_class=multi_class,
        verbose=verbose,
        warm_start=warm_start,
        n_jobs=n_jobs,
        l1_ratio=l1_ratio,
    ).fit(x, y)

    return pd.DataFrame(
        model.predict(data_frame), columns=[f"{p}_predict" for p in predictors]
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
        "-off",
        "--offset",
        type=int,
        default=1,
        help="""Offset for predict (p.ex. if 1 regressor [:-1] predictor [1:])
        (default: 1).""",
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
        "-r",
        "--regressors",
        type=str,
        nargs="*",
        help="an string for the header (regressors) in the dataset",
    )
    ap.add_argument(
        "-p",
        "--predictors",
        type=str,
        nargs="+",
        help="an string for the header (predictors) in the dataset",
    )
    ap.add_argument("--penalty", type=str, default="l2")
    ap.add_argument("--dual", type=bool, default=False)
    ap.add_argument("--tol", type=float, default=1e-4)
    ap.add_argument("--C", type=float, default=1.0)
    ap.add_argument("--fit-intercept", type=bool, default=True)
    ap.add_argument("--intercept-scaling", type=float, default=1)
    ap.add_argument("--class-weight", type=dict or str, default=None)
    ap.add_argument("--random_state", type=int or str, default=None)
    ap.add_argument("--solver", type=str, default="liblinear")
    ap.add_argument("--max-iter", type=int, default=100)
    ap.add_argument("--multi-class", type=str, default="ovr")
    ap.add_argument("--verbose", type=int, default=0)
    ap.add_argument("--warm-start", type=bool, default=False)
    ap.add_argument("--n-jobs", type=int, default=None)
    ap.add_argument("--l1-ratio", type=float, default=None)
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply
    result = logistic_regression(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        penalty=args["penalty"],
        dual=args["dual"],
        tol=args["tol"],
        C=args["C"],
        fit_intercept=args["fit_intercept"],
        intercept_scaling=args["intercept_scaling"],
        class_weight=args["class_weight"],
        random_state=args["random_state"],
        solver=args["solver"],
        max_iter=args["max_iter"],
        multi_class=args["multi_class"],
        verbose=args["verbose"],
        warm_start=args["warm_start"],
        n_jobs=args["n_jobs"],
        l1_ratio=args["l1_ratio"],
        offset=args["offset"],
        regressors=args["regressors"],
        predictors=args["predictors"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
