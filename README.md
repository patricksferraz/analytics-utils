# ANALYTICS-UTILS

Package contain function for data analytics

## Installing

```sh
pip install analytics-utils
```

## Usage

### describe_data

This function describe the datas of a dataframe. Returning the max, min, mean, median, quantile, variance, standard deviation, mean, absolute deviation, amplitude, root mean squared, kurtosis, skewness and count for all headers in dataframe

#### function

```python
from analytics_utils.describe_data import describe_data

describe_data(dataframe, headers, lang)
```

- dataframe: dataframe for describe
- headers: columns of dataframe for describe. Returnered descriptions:

  - maximum
  - minimum
  - mean
  - median
  - [1|3]-quartile
  - variance
  - standard deviation
  - mean absolute deviation
  - amplitude
  - root mean squared
  - kurtosis
  - skewness
  - count

- lang: output language (default: 'pt')

  - 'pt': portuguese
  - 'en': english

#### terminal

- **Help message**

```sh
usage: describe_data.py [-h] -d DATASET [-f FILE_OUT] [-o ORIENT] [-l LANG]
                        [-pd [PARSE_DATES [PARSE_DATES ...]]]
                        [-i [INDEX [INDEX ...]]] [-hd [H [H ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        path to input dataset
  -f FILE_OUT, --file-out FILE_OUT
                        path to file of output json
  -o ORIENT, --orient ORIENT
                        format json output {'split', 'records', 'index',
                        'values', 'table', 'columns'} (default: 'columns')
  -l LANG, --lang LANG  language for the output result {'pt', 'en'} (default:
                        'pt')
  -pd [PARSE_DATES [PARSE_DATES ...]], --parse-dates [PARSE_DATES [PARSE_DATES ...]]
                        Headers of columns to parse dates. A column named
                        datetime is created.
  -i [INDEX [INDEX ...]], --index [INDEX [INDEX ...]]
                        Headers of columns to set as index.
  -hd [H [H ...]], --headers [H [H ...]]
                        an string for the header in the dataset
```

- **Usage**

```sh
python describe_data.py -d dataset.csv -pd date time -i datetime -f out.json
```

### correlate

This function returns the correlation between the columns of a dataframe. This is the same corr function in pandas package.

#### function

```python
from analytics_utils.correlate import correlate

correlate(dataframe, method, min_periods)
```

- dataframe: correlation dataframe
- method: correlation method (default: {"pearson"}):

  - pearson
  - kendall
  - spearman
  - or callable with input two 1d ndarrays

- min_periods: Minimum number of observations required per pair of columns to have a valid result. Currently only available for Pearson and Spearman correlation (default: {1}).

#### terminal

- **Help message**

```sh
usage: correlate.py [-h] -d DATASET [-f FILE_OUT] [-o ORIENT] [-m METHOD]
                    [-p MIN_PERIODS]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        path to input dataset
  -f FILE_OUT, --file-out FILE_OUT
                        path to file of output json
  -o ORIENT, --orient ORIENT
                        format json output {'split', 'records', 'index',
                        'values', 'table', 'columns'} (default: 'columns')
  -m METHOD, --method METHOD
                        method of correlation {‘pearson’, ‘kendall’,
                        ‘spearman’} (default: 'pearson')
  -p MIN_PERIODS, --min-periods MIN_PERIODS
                        Minimum number of observations required per pair of
                        columns to have a valid result. Currently only
                        available for Pearson and Spearman correlation
                        (default: 1).
```

- **Usage**

```sh
python correlate.py -d dataset.csv -f out.json
```

### interpolate

This function returns the Series or DataFrame of same shape interpolated at the NaNs. This is a adapted interpolate function of pandas package.

#### function

```python
from analytics_utils.interpolate import interpolate

interpolate(dataframe, headers, method, limit)
```

- dataframe: dataframe for interpolation
- headers: columns of dataframe for interpolating (default: {None}). For default, all are interpolated.
- method: interpolation method. Please note that only method='linear' is supported for DataFrame/Series with a MultiIndex. (default: {"linear"}):

  - linear
  - time
  - index
  - values
  - nearest
  - zero
  - slinear
  - quadratic
  - cubic
  - barycentric
  - krogh
  - polynomial
  - spline
  - piecewise_polynomial
  - pchip

- limit: Maximum number of consecutive NaNs to fill (default: {None}).

#### terminal

- **Help message**

```sh
usage: interpolate.py [-h] -d DATASET [-f FILE_OUT] [-o ORIENT] [-m METHOD]
                      [-l LIMIT] [-pd [PARSE_DATES [PARSE_DATES ...]]]
                      [-i [INDEX [INDEX ...]]] [-hd [H [H ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        path to input dataset
  -f FILE_OUT, --file-out FILE_OUT
                        path to file of output json
  -o ORIENT, --orient ORIENT
                        format json output {'split', 'records', 'index',
                        'values', 'table', 'columns'} (default: 'columns')
  -m METHOD, --method METHOD
                        method of interpolation. Please note that only
                        method='linear' is supported for DataFrame/Series with
                        a MultiIndex. {‘linear’, ‘time’, ‘index’, ‘values’,
                        ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’,
                        ‘barycentric’, ‘krogh’, ‘polynomial’, ‘spline’
                        ‘piecewise_polynomial’, ‘pchip’} (default: 'linear')
  -l LIMIT, --limit LIMIT
                        Maximum number of consecutive NaNs to fill (default:
                        None)
  -pd [PARSE_DATES [PARSE_DATES ...]], --parse-dates [PARSE_DATES [PARSE_DATES ...]]
                        Headers of columns to parse dates. A column named
                        datetime is created.
  -i [INDEX [INDEX ...]], --index [INDEX [INDEX ...]]
                        Headers of columns to set as index.
  -hd [H [H ...]], --headers [H [H ...]]
                        an string for the header in the dataset
```

- **Usage**

```sh
python analytics-utils/interpolate.py -d dataset.csv -f out.json
```

### rolling window

This function Provide rolling window calculations. This is a adapted rolling function of pandas package.

#### function

```python
from analytics_utils.roll import roll

roll(dataframe, window, roll_type, headers)
```

- dataframe: dataframe for apply rolling
- window: Size of the moving window. This is the number of observations used for calculating the statistic. Each window will be a fixed size.
- roll_type: rolling method (default: {"mean"}):

  - mean
  - var (variance)
  - std (standard deviation)

#### terminal

- **Help message**

```sh
usage: roll.py [-h] -d DATASET [-f FILE_OUT] [-o ORIENT] -w WINDOW
               [-t ROLL_TYPE] [-pd [PARSE_DATES [PARSE_DATES ...]]]
               [-i [INDEX [INDEX ...]]] [-hd [HEADERS [HEADERS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        path to input dataset
  -f FILE_OUT, --file-out FILE_OUT
                        path to file of output json
  -o ORIENT, --orient ORIENT
                        format json output {'split', 'records', 'index',
                        'values', 'table', 'columns'} (default: 'columns')
  -w WINDOW, --window WINDOW
                        Size of the moving window. This is the number of
                        observations used for calculating the statistic. Each
                        window will be a fixed size.
  -t ROLL_TYPE, --roll_type ROLL_TYPE
                        {‘mean’, ‘var’, 'std'} (default: {"mean"}).
  -pd [PARSE_DATES [PARSE_DATES ...]], --parse-dates [PARSE_DATES [PARSE_DATES ...]]
                        Headers of columns to parse dates. A column named
                        datetime is created.
  -i [INDEX [INDEX ...]], --index [INDEX [INDEX ...]]
                        Headers of columns to set as index.
  -hd [HEADERS [HEADERS ...]], --headers [HEADERS [HEADERS ...]]
                        an string for the header in the dataset
```

- **Usage**

```sh
python analytics-utils/roll.py -w 12 -d dataset.csv -f out.json
```

### exponential weighted moving

This function provide exponential weighted functions. This is a adapted ewm function of pandas package.

#### function

```python
from analytics_utils.ewm import ewm

ewm(dataframe, com, span, halflife, alpha, ignore_na, ewm_type, headers)
```

- dataframe: dataframe for apply ewm
- com: specify decay in terms of center of mass, α=1/(1+com), for com≥0 (default: {None}).
- span: specify decay in terms of span, α=2/(span+1), for span≥1 (default: {None}).
- halflife: specify decay in terms of half-life, α=1−exp(log(0.5)/halflife),for halflife>0 (default: {None}).
- alpha: specify smoothing factor α directly, 0<α≤1 (default: {None}).
- ignore_na: ignore missing values when calculating weights; specify True to reproduce pre-0.15.0 behavior (default: {False}).
- ewm_type: ewm method (default: {"mean"}):

  - mean
  - var (variance)
  - std (standard deviation)

- headers: columns of dataframe for apply ewm (default: {None}).

#### terminal

- **Help message**

```sh
usage: ewm.py [-h] -d DATASET [-f FILE_OUT] [-o ORIENT] [-c COM] [-s SPAN]
              [-hl HALFLIFE] [-a ALPHA] [-ina IGNORE_NA] [-t EWM_TYPE]
              [-pd [PARSE_DATES [PARSE_DATES ...]]] [-i [INDEX [INDEX ...]]]
              [-hd [HEADERS [HEADERS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        path to input dataset
  -f FILE_OUT, --file-out FILE_OUT
                        path to file of output json
  -o ORIENT, --orient ORIENT
                        format json output {'split', 'records', 'index',
                        'values', 'table', 'columns'} (default: 'columns')
  -c COM, --com COM     Specify decay in terms of center of mass, α=1/(1+com),
                        for com≥0 (default: None).
  -s SPAN, --span SPAN  Specify decay in terms of span, α=2/(span+1), for
                        span≥1 (default: None).
  -hl HALFLIFE, --halflife HALFLIFE
                        Specify decay in terms of half-life,
                        α=1−exp(log(0.5)/halflife) , for halflife>0 (default:
                        None).
  -a ALPHA, --alpha ALPHA
                        Specify smoothing factor α directly, 0<α≤1 (default:
                        None).
  -ina IGNORE_NA, --ignore-na IGNORE_NA
                        Ignore missing values when calculating weights;
                        specify True to reproduce (default: False).
  -t EWM_TYPE, --ewm-type EWM_TYPE
                        {‘mean’, ‘var’, 'std'} (default: {"mean"}).
  -pd [PARSE_DATES [PARSE_DATES ...]], --parse-dates [PARSE_DATES [PARSE_DATES ...]]
                        Headers of columns to parse dates. A column named
                        datetime is created.
  -i [INDEX [INDEX ...]], --index [INDEX [INDEX ...]]
                        Headers of columns to set as index.
  -hd [HEADERS [HEADERS ...]], --headers [HEADERS [HEADERS ...]]
                        an string for the header in the dataset
```

- **Usage**

```sh
python analytics-utils/ewm.py -hl 12 -d dataset.csv -f out.json
```

### seasonal decompose

Seasonal decomposition using moving averages. This is a adapted seasonal_decompose function of statsmodels package.

#### function

```python
from analytics_utils.decompose import decompose

decompose(dataframe, model, filt, freq, two_sided, extrapolate_trend, lang, headers)
```

- dataframe: dataframe for apply decompose
- model: Type of seasonal component. Abbreviations are accepted (default: {'additive'}).

  - additive
  - multiplicative

- filt: The filter coefficients for filtering out the seasonal component. The concrete moving average method used in filtering is determined by two_sided (default: {None}).
- freq: Frequency of the series. Must be used if x is not a pandas object. Overrides default periodicity of x if x is a pandas object with a timeseries index (default: {None}).
- two_sided: The moving average method used in filtering. If True (default), a centered moving average is computed using the filt. If False, the filter coefficients are for past values only (default: {True}).
- extrapolate_trend: If set to > 0, the trend resulting from the convolution is linear least-squares extrapolated on both ends (or the single one if two_sided is False) considering this many (+1) closest points. If set to 'freq', use freq closest points. Setting this parameter results in no NaN values in trend or resid components (default: {0}).
- headers: columns of dataframe for apply ewm (default: {None}).

#### terminal

- **Help message**

```sh
usage: decompose.py [-h] -d DATASET [-f FILE_OUT] [-o ORIENT] [-m MODEL]
                    [-ft [FILT [FILT ...]]] [-fq FREQ] [-t TWO_SIDED]
                    [-e EXTRAPOLATE_TREND] [-l LANG]
                    [-pd [PARSE_DATES [PARSE_DATES ...]]]
                    [-i [INDEX [INDEX ...]]] [-hd [HEADERS [HEADERS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        path to input dataset
  -f FILE_OUT, --file-out FILE_OUT
                        path to file of output json
  -o ORIENT, --orient ORIENT
                        format json output {'split', 'records', 'index',
                        'values', 'table', 'columns'} (default: 'columns')
  -m MODEL, --model MODEL
                        Type of seasonal component. Abbreviations are accepted
                        (default: 'additive').
  -ft [FILT [FILT ...]], --filt [FILT [FILT ...]]
                        The filter coefficients for filtering out the seasonal
                        component. The concrete moving average method used in
                        filtering is determined by two_sided (default: None).
  -fq FREQ, --freq FREQ
                        Frequency of the series. Must be used if x is not a
                        pandas object. Overrides default periodicity of x if x
                        is a pandas object with a timeseries index (default:
                        None).
  -t TWO_SIDED, --two-sided TWO_SIDED
                        The moving average method used in filtering. If True
                        (default), a centered moving average is computed using
                        the filt. If False, the filter coefficients are for
                        past values only (default: True).
  -e EXTRAPOLATE_TREND, --extrapolate-trend EXTRAPOLATE_TREND
                        If set to > 0, the trend resulting from the
                        convolution is linear least-squares extrapolated on
                        both ends (or the single one if two_sided is False)
                        considering this many (+1) closest points. If set to
                        ‘freq’, use freq closest points. Setting this
                        parameter results in no NaN values in trend or resid
                        components (default: 0).
  -l LANG, --lang LANG  language for the output result {'pt', 'en'} (default:
                        'pt')
  -pd [PARSE_DATES [PARSE_DATES ...]], --parse-dates [PARSE_DATES [PARSE_DATES ...]]
                        Headers of columns to parse dates. A column named
                        datetime is created.
  -i [INDEX [INDEX ...]], --index [INDEX [INDEX ...]]
                        Headers of columns to set as index.
  -hd [HEADERS [HEADERS ...]], --headers [HEADERS [HEADERS ...]]
                        an string for the header in the dataset
```

- **Usage**

```sh
python analytics-utils/decompose.py -pd date time -i datetime -fq 12 -d dataset.csv -f out.json
```
