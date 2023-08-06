import numpy as np


class RSI:
    """
    A class used to calculate the Relative Strength Index (RSI) indicator.

    Attributes
        close_prices : Union[List[float], np.ndarray]
            List or numpy array of close prices for the asset.
        period : int, optional
            The number of periods used for the RSI calculation. Default is 14.

    Methods
        calculate_rsi(output_type='float') : Union[float, np.ndarray]
            Calculate the RSI value(s) for the given close prices.

    """

    def __init__(self, close_prices=[], period=14):
        """
        Constructor for the RSI class with the given close prices and period.

        Parameters
            close_prices : Union[List[float], np.ndarray]
                List or numpy array of close prices for the asset.
            period : int, optional
                The number of periods used for the RSI calculation. Default is 14.
        """
        # Validate inputs
        if len(close_prices) < period:
            raise ValueError("close_prices must be at least length period.")
        if not isinstance(close_prices, (list, np.ndarray)):
            raise ValueError("close_prices must be a list or a numpy array.")
        if not isinstance(period, int) or period < 1:
            raise ValueError("period must be a positive integer.")

        # Convert data to numpy array
        if isinstance(close_prices, list):
            self.close_prices = np.array(close_prices)
        else:
            self.close_prices = close_prices

        self.period = period

    def calculate_rsi(self, output_type='float'):
        """
        Calculates the Relative Strength Index (RSI) for the given close prices and period.

        Parameters
            output_type : string, optional
                The types of output to return possible values are 'float' or 'numpy_array'. 
                If 'float', returns the RSI value as a float.
                If 'numpy_array', returns the RSI values as a numpy array of the same length as the input prices.
                Default is 'float'.

        Returns
            float or numpy.ndarray : The RSI value as a float if output_type is 'float', 
                                     otherwise the RSI values as a numpy array.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """
        # Calculate price changes
        deltas = np.diff(self.close_prices)
        seed = deltas[:self.period + 1]

        # Separate gains and losses
        up = seed[seed >= 0].sum() / self.period
        down = -seed[seed < 0].sum() / self.period

        rs_values = np.zeros_like(self.close_prices, dtype=float)
        rs_values[:self.period] = 100.0

        # Calculate RSI for the remaining prices
        for i in range(self.period, len(self.close_prices)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up * (self.period - 1) + upval) / float(self.period)
            down = (down * (self.period - 1) + downval) / float(self.period)

            # Avoid division by zero
            if down == 0:
                rs = 100.0
            else:
                rs = up / down

            rsi = 100. - 100. / (1. + rs)
            rs_values[i] = rsi

        if output_type == 'float':
            return rs_values[-1]
        elif output_type == 'numpy_array':
            return rs_values
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )
