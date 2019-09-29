# -*- coding: utf-8 -*-
"""
This is the find module.
The find module supplies one function,
    arima()
"""

import matplotlib.pyplot as plt
import pmdarima as pm
import pandas as pd
import numpy as np


def arima(
    data_frame: pd.DataFrame,
    exogenous: [] = None,
    start_p: int = 2,
    d: int = None,
    start_q: int = 2,
    max_p: int = 5,
    max_d: int = 2,
    max_q: int = 5,
    start_P: int = 1,
    D: int = None,
    start_Q: int = 1,
    max_P: int = 2,
    max_D: int = 1,
    max_Q: int = 2,
    max_order: int = 10,
    m: int = 1,
    seasonal: bool = True,
    stationary: bool = False,
    information_criterion: str = "aic",
    alpha: float = 0.05,
    test: str = "kpss",
    seasonal_test: str = "ocsb",
    stepwise: bool = True,
    n_jobs: int = 1,
    start_params: [] = None,
    trend: str = None,
    method: str = None,
    transparams: bool = True,
    solver: str = "lbfgs",
    maxiter: int = None,
    disp: int = 0,
    callback=None,
    offset_test_args: dict = None,
    seasonal_test_args: dict = None,
    suppress_warnings: bool = False,
    error_action: str = "warn",
    trace: bool = False,
    random: bool = False,
    random_state: int = None,
    n_fits: int = 10,
    return_valid_fits: bool = False,
    out_of_sample_size: int = 0,
    scoring: str = "mse",
    scoring_args: dict = None,
    with_intercept: bool = True,
    sarimax_kwargs: dict = None,
    time_step: int = 1,
    report: bool = False,
    return_conf_int: bool = False,
    regressors: [str] = None,
    **fit_args,
) -> pd.DataFrame:
    """Ordinary least squares Linear RegressionAutomatically discover the
    optimal order for an ARIMA model.. This is a adapted auto_arima function of
    pmdarima package.

    Arguments:
        data_frame {pd.DataFrame} -- input dataframe

    Keyword Arguments:
        time_step {int} -- Period for predict (p.ex. if 1 predict for next 1
            period) (default: {1})
        report {bool} -- If True, print summary of train and plot model
            diagnostics (default: {False})
        return_conf_int {bool} -- If True, return confidence interval of each
            regressor (default: {False})
        regressors {[str]} -- chosen dataframe headers for regressor
            (default: {None}).

        {others params} -- See pmdarima.arima.auto_arima

    Raises:
        ValueError: Offset cannot be less than 1
        ValueError: Predictors cannot be None

    Returns:
        pd.DataFrame -- Returns predicted values with confidence interval (if
        return_cond_int is True).
    """

    if time_step < 1:
        raise ValueError("Offset cannot be less than 1")

    if regressors:
        data_frame = data_frame.loc[:, regressors]

    df = pd.DataFrame()
    for column in data_frame:
        model = pm.auto_arima(
            data_frame[column],
            exogenous=exogenous,
            start_p=start_p,
            d=d,
            start_q=start_q,
            max_p=max_p,
            max_d=max_d,
            max_q=max_q,
            start_P=start_P,
            D=D,
            start_Q=start_Q,
            max_P=max_P,
            max_D=max_D,
            max_Q=max_Q,
            max_order=max_order,
            m=m,
            seasonal=seasonal,
            stationary=stationary,
            information_criterion=information_criterion,
            alpha=alpha,
            test=test,
            seasonal_test=seasonal_test,
            stepwise=stepwise,
            n_jobs=n_jobs,
            start_params=start_params,
            trend=trend,
            method=method,
            transparams=transparams,
            solver=solver,
            maxiter=maxiter,
            disp=disp,
            callback=callback,
            offset_test_args=offset_test_args,
            seasonal_test_args=seasonal_test_args,
            suppress_warnings=suppress_warnings,
            error_action=error_action,
            trace=trace,
            random=random,
            random_state=random_state,
            n_fits=n_fits,
            return_valid_fits=return_valid_fits,
            out_of_sample_size=out_of_sample_size,
            scoring=scoring,
            scoring_args=scoring_args,
            with_intercept=with_intercept,
            sarimax_kwargs=sarimax_kwargs,
            **fit_args,
        )

        # Report
        if report:
            print(f"REPORT({column})")
            print(model.summary())
            model.plot_diagnostics()
            plt.show()

        # Forecasting
        predict = model.predict(
            n_periods=time_step, return_conf_int=return_conf_int
        )

        # Confidence interval (lconf = lower conf; uconf = upper conf)
        conf = None
        if return_conf_int:
            conf = np.array(predict[1])
            conf = pd.DataFrame(
                {f"{column}_lconf": conf[:, 0], f"{column}_uconf": conf[:, 1]}
            )
            predict = predict[0]

        # Concatenate
        predict = pd.DataFrame({f"{column}_pred": predict})
        df = pd.concat([df, predict, conf], axis=1)

    return df


if __name__ == "__main__":
    import argparse
    import json

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
        "-p",
        "--n-periods",
        type=int,
        default=1,
        help="""Period for predict (p.ex. if 1 predict for next 1 period)
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
    ap.add_argument("--exogenous", nargs="*")
    ap.add_argument("--start-p", type=int, default=2)
    ap.add_argument("--d", type=int, default=None)
    ap.add_argument("--start-q", type=int, default=2)
    ap.add_argument("--max-p", type=int, default=5)
    ap.add_argument("--max-d", type=int, default=2)
    ap.add_argument("--max-q", type=int, default=5)
    ap.add_argument("--start-P", type=int, default=1)
    ap.add_argument("--D", type=int, default=None)
    ap.add_argument("--start-Q", type=int, default=1)
    ap.add_argument("--max-P", type=int, default=2)
    ap.add_argument("--max-D", type=int, default=1)
    ap.add_argument("--max-Q", type=int, default=2)
    ap.add_argument("--max-order", type=int, default=10)
    ap.add_argument("--m", type=int, default=1)
    ap.add_argument("--seasonal", type=bool, default=True)
    ap.add_argument("--stationary", type=bool, default=False)
    ap.add_argument("--information_criterion", type=str, default="aic")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--test", type=str, default="kpss")
    ap.add_argument("--seasonal-test", type=str, default="ocsb")
    ap.add_argument("--stepwise", type=bool, default=True)
    ap.add_argument("--n-jobs", type=int, default=1)
    ap.add_argument("--start_params", nargs="*")
    ap.add_argument("--trend", type=str, default=None)
    ap.add_argument("--method", type=str, default=None)
    ap.add_argument("--transparams", type=bool, default=True)
    ap.add_argument("--solver", type=str, default="lbfgs")
    ap.add_argument("--maxiter", type=int, default=None)
    ap.add_argument("--disp", type=int, default=0)
    ap.add_argument("--offset-test-args", type=json.loads, default=None)
    ap.add_argument("--seasonal-test-args", type=json.loads, default=None)
    ap.add_argument("--suppress-warnings", type=bool, default=False)
    ap.add_argument("--error-action", type=str, default="warn")
    ap.add_argument("--trace", type=bool, default=False)
    ap.add_argument("--random", type=bool, default=False)
    ap.add_argument("--random-state", type=int, default=None)
    ap.add_argument("--n-fits", type=int, default=10)
    ap.add_argument("--return-valid-fits", type=bool, default=False)
    ap.add_argument("--out-of-sample-size", type=int, default=0)
    ap.add_argument("--scoring", type=str, default="mse")
    ap.add_argument("--scoring-args", type=json.loads, default=None)
    ap.add_argument("--with-intercept", type=bool, default=True)
    ap.add_argument("--sarimax-kwargs", type=json.loads, default=None)
    ap.add_argument("--report", type=bool, default=False)
    ap.add_argument("--return-conf-int", type=bool, default=False)
    ap.add_argument("--fit-args", type=json.loads, default=None)
    args = vars(ap.parse_args())

    # If exist parse_dates, creates a structure with column name datetime
    if args["parse_dates"]:
        args["parse_dates"] = {"datetime": args["parse_dates"]}

    # Apply arima
    result = arima(
        pd.read_csv(
            args["dataset"],
            parse_dates=args["parse_dates"],
            index_col=args["index"],
        ),
        exogenous=args["exogenous"],
        start_p=args["start_p"],
        d=args["d"],
        start_q=args["start_q"],
        max_p=args["max_p"],
        max_d=args["max_d"],
        max_q=args["max_q"],
        start_P=args["start_P"],
        D=args["D"],
        start_Q=args["start_Q"],
        max_P=args["max_P"],
        max_D=args["max_D"],
        max_Q=args["max_Q"],
        max_order=args["max_order"],
        m=args["m"],
        seasonal=args["seasonal"],
        stationary=args["stationary"],
        information_criterion=args["information_criterion"],
        alpha=args["alpha"],
        test=args["test"],
        seasonal_test=args["seasonal_test"],
        stepwise=args["stepwise"],
        n_jobs=args["n_jobs"],
        start_params=args["start_params"],
        trend=args["trend"],
        method=args["method"],
        transparams=args["transparams"],
        solver=args["solver"],
        maxiter=args["maxiter"],
        disp=args["disp"],
        offset_test_args=args["offset_test_args"],
        seasonal_test_args=args["seasonal_test_args"],
        suppress_warnings=args["suppress_warnings"],
        error_action=args["error_action"],
        trace=args["trace"],
        random=args["random"],
        random_state=args["random_state"],
        n_fits=args["n_fits"],
        return_valid_fits=args["return_valid_fits"],
        out_of_sample_size=args["out_of_sample_size"],
        scoring=args["scoring"],
        scoring_args=args["scoring_args"],
        with_intercept=args["with_intercept"],
        sarimax_kwargs=args["sarimax_kwargs"],
        report=args["report"],
        return_conf_int=args["return_conf_int"],
        time_step=args["time_step"],
        regressors=args["regressors"],
        **args["fit_args"],
    )

    # Output in json format
    result = result.to_json(
        args.get("file_out"), force_ascii=False, orient=args["orient"]
    )
    if result:
        print(result)
