# Technical Indicator Python Package

This Python package provides methods to calculate various technical indicators from financial time series datasets. The indicators are organized into four categories: momentum indicators, trend indicators, volume indicators, and volatility indicators.

### Installation

You can install the Technical Indicator package using pip:

```
pip install technical-indicator
```

### Momentum Indicators

#### Relative Strength Index (RSI)

The RSI measures the ratio of upward price movements to downward price movements over a given period of time. To calculate the RSI using this package, initialize an instance of the RSI class with an array of close prices and an optional lookback period (default is 14), and call the calculate method:

```
from technical_indicator.momentum import RSI

# Example data
period = 12
close_prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20, 18, 16, 17, 15, 17, 19, 20, 16, 17, 18, 14, 20, 18]

# Initialize the RSI indicator with the prices and period
rsi = RSI(close_prices, period)

# Calculate the RSI values
rsi_values = rsi.calculate_rsi()
```

#### Moving Average Convergence Divergence (MACD)

The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price. To calculate the MACD using this package, initialize an instance of the MACD class with an array of close prices and optional fast and slow lookback periods (default are 12 and 26, respectively), and call the calculate method:

```
from technical_indicator.momentum import MACD

# Example data
fast_period = 12
slow_period = 26
close_prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20, 18, 16, 17, 15, 17, 19, 20, 16, 17, 18, 14, 20, 18]

# Initialize the MACD indicator with the prices and periods
macd = MACD(close_prices, fast_period, slow_period)

# Calculate the MACD values
macd_values = macd.calculate_macd()
```

#### MACD Histogram

The MACD (Moving Average Convergence Divergence) Histogram is a momentum indicator that shows the difference between the MACD line and the signal line. It is derived from the MACD line and is used to identify potential trend reversals. To calculate the MACD Histogram using this package, import the MACDHistogram class from the momentum module, initialize an instance with an array of close prices and optional parameters, and call the calculate method:

```
from technical_indicator.momentum import MACDHistogram

# Example data
close_prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20, 18, 16, 17, 15, 17, 19, 20, 16, 17, 18, 14, 20, 18]
fast_period = 6
slow_period = 12
signal_period = 9

# Initialize the MACD Histogram indicator with the prices and periods
macd_histogram = MACDHistogram(close_prices, fast_period, slow_period, signal_period)

# Calculate the MACD Histogram values
macd_histogram_values = macd_histogram.calculate_macd_histogram()
```

### Trend Indicators

#### Simple Moving Average (SMA)

The Simple Moving Average (SMA) is a widely used technical indicator that represents the average closing price of a security over a specified period of time. To calculate the SMA using this package, initialize an instance of the MovingAverage class with an array of close prices and an optional lookback period (default is 9), and call the calculate method:

```
from technical_indicator.trend import MovingAverage

# Example data
period = 20
close_prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20, 18, 16, 17, 15, 17, 19, 20, 16, 17, 18, 14, 20, 18]

# Initialize the MovingAverage instance with the prices and period
ma = MovingAverage(close_prices, period)

# Calculate the SMA values
sma_values = ma.calculate_sma()
```

#### Exponential Moving Average (EMA)

The Exponential Moving Average (EMA) is a type of moving average that gives more weight to recent prices. To calculate the EMA using this package, initialize an instance of the MovingAverage class with an array of close prices and an optional lookback period (default is 9), and call the calculate method:

```
from technical_indicator.trend import MovingAverage

# Example data
period = 20
close_prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20, 18, 16, 17, 15, 17, 19, 20, 16, 17, 18, 14, 20, 18]

# Initialize the MovingAverage instance with the prices and period
ma = MovingAverage(close_prices, period)

# Calculate the EMA values
ema_values = ma.calculate_ema()
```

#### Weighted Moving Average (WMA)

The Weighted Moving Average (WMA) is a type of moving average that gives more weight to recent prices while allowing the user to specify the exact weighting of each price in the calculation. To calculate the WMA using this package, initialize an instance of the MovingAverage class with an array of close prices and call the calculate_wma method:

```
from technical_indicator.trend import MovingAverage

# Example data
period = 20
close_prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20, 18, 16, 17, 15, 17, 19, 20, 16, 17 , 18, 14, 20, 18]

# Initialize the MovingAverage instance with the prices and period
ma = MovingAverage(close_prices, period)

# Calculate the WMA value
wma_value = ma.calculate_wma()
```

#### Hull Moving Average (HMA)

The Hull Moving Average (HMA) is a type of moving average that aims to reduce the lag and noise of traditional moving averages while maintaining smoothness. To calculate the HMA using this package, initialize an instance of the MovingAverage class with an array of close prices and an optional lookback period (default is 9), and call the calculate_hma method:

```
from technical_indicator.trend import MovingAverage

# Example data
period = 20
close_prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20, 18, 16, 17, 15, 17, 19, 20, 16, 17 , 18, 14, 20, 18]

# Initialize the MovingAverage instance with the prices and period
ma = MovingAverage(close_prices, period)

# Calculate the HMA values
hma_values = ma.calculate_hma()
```
