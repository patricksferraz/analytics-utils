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

### correlation

This function returns the correlation between the columns of a dataframe. This is the same corr function in pandas package.

```python
from analytics_utils.correlation import correlation

correlation(dataframe, method, min_periods)
```

- dataframe: correlation dataframe
- method: correlation method (default: {"pearson"}):

  - pearson
  - kendall
  - spearman
  - or callable with input two 1d ndarrays

- min_periods: Minimum number of observations required per pair of columns to have a valid result. Currently only available for Pearson and Spearman correlation (default: {1}).
