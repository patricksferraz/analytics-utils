# ANALYTICS-UTILS

Package contain function for data analytics

## Installing

```sh
pip install analytics-utils
```

## Usage

### describe_data

This function describe the datas of a dataframe. Returning the max, min, mean, median, quantile, variance, standard deviation, mean, absolute deviation, amplitude, root mean squared, kurtosis, skewness and count for all headers in dataframe

#### Function

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

#### Terminal

- **Help message**

````sh
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
                        "format json output {'split', 'records', 'index',
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

```python
from analytics_utils.correlate import correlate

correlate(dataframe, method, min_periods)
````

- dataframe: correlation dataframe
- method: correlation method (default: {"pearson"}):

  - pearson
  - kendall
  - spearman
  - or callable with input two 1d ndarrays

- min_periods: Minimum number of observations required per pair of columns to have a valid result. Currently only available for Pearson and Spearman correlation (default: {1}).

### interpolate

This function returns the Series or DataFrame of same shape interpolated at the NaNs. This is a adapted interpolate function of pandas package.

```python
from analytics_utils.interpolate import interpolate

interpolate(dataframe, headers, method, limit)
```

- dataframe: dataframe for interpolation
- headers: columns of dataframe for interpolating (default: {None}). For default, all are interpolated.
- method: interpolation method (default: {"linear"}):

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
