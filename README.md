# ANALYTICS-UTILS

Package contain function for data analytics

## Installing

```sh
pip install analytics-utils
```

## Usage

### describe_data

This function describe the datas of a dataframe. Returning the max, min, mean, median, quantile, variance, standard deviation, mean, absolute deviation, amplitude, root mean squared, kurtosis, skewness and count for all headers in dataframe

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

### correlate

This function returns the correlation between the columns of a dataframe. This is the same corr function in pandas package.

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
