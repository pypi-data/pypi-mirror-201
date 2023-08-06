import numpy as np
from .calculate_macd import MACD


class MACDHistogram:
    """
    A class used to calculate the Moving Average Convergence Divergence (MACD) Histogram indicator.

    Attributes
        close_prices : Union[List[float], np.ndarray]
            A list or numpy array of the given close prices for the asset.
        fast_period : int, optional
            The number of time periods used for the fast EMA calculation.
        slow_period : int, optional
            The number of time periods used for the slow EMA calculation.
        signal_period : int, optional
            The number of time periods used for the signal line calculation.

    Methods
        calculate_macd_histogram(output_type='float') : Union[float, np.ndarray]
            Calculate the MACD Histogram value(s) for the given close prices.
    """

    def __init__(self,
                 close_prices,
                 fast_period=12,
                 slow_period=26,
                 signal_period=9):
        """
        Constructor for the MACDHistogram class.

        Parameters
            close_prices : Union[List[float], np.ndarray]
                A list or numpy array of the given close prices for the asset.
            fast_period : int, optional
                The number of time periods used for the fast EMA calculation. Default is 12.
            slow_period : int, optional
                The number of time periods used for the slow EMA calculation. Default is 26.
            signal_period : int, optional
                The number of time periods used for the signal line calculation. Default is 9.
        """
        # Convert data to numpy array
        if isinstance(close_prices, list):
            self.close_prices = np.array(close_prices)
        else:
            self.close_prices = close_prices

        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def calculate_macd_histogram(self, output_type='float'):
        """
        Calculate the MACD Histogram, which is the difference between the MACD line and the signal line.

        Parameters
            output_type : string, optional
                The types of output to return possible values are 'float' or 'numpy_array'. 
                If 'float', returns the MACD Histogram value as a float.
                If 'numpy_array', returns the MACD Histogram values as a numpy array of the same length as the input prices.
                Default is 'float'.

        Returns
            float or numpy.ndarray : The MACD Histogram value as a float if output_type is 'float', otherwise the MACD Histogram values as a 
                    numpy array.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """

        macd = MACD(
            self.close_prices, self.fast_period, self.slow_period,
            self.signal_period).calculate_macd(output_type='numpy_array')

        signal_line = MACD(self.close_prices, self.fast_period,
                           self.slow_period,
                           self.signal_period).calculate_signal_line(
                               output_type='numpy_array')

        # Calculate the difference between the MACD line and the signal line
        histogram = macd - signal_line

        if output_type == 'float':
            return float(histogram[-1])
        elif output_type == 'numpy_array':
            return histogram
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )
