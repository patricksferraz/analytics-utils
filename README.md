# ANALYTICS-UTILS

Package contain function for data analytics

## Installing

```sh
$ pip install analytics-utils
```

## Usage

### describe_data

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
  - [1|3]-quantile
  - variance
  - standard deviation
  - mean absolute deviation
  - amplitude
  - root mean squared
  - kurtosis
  - skewness
  - count

- lang: output language ['pt':portuguese (default) | 'en':english]
