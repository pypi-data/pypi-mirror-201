import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trend.calculate_moving_average import MovingAverage


class MACD:
    """
    A class used to calculate Moving Average Convergence Divergence (MACD) indicator.

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
        calculate_macd(output_type='float') : Union[float, np.ndarray]
            Calculate the MACD value(s) for the given close prices.
        calculate_signal_line(output_type='float') : Union[float, np.ndarray]
            Calculate the Signal value(s) for the given close prices.
    """

    def __init__(self,
                 close_prices=[],
                 fast_period=12,
                 slow_period=26,
                 signal_period=9):
        """
        Constructor for the MACD class.

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

    def calculate_macd(self, output_type='float'):
        """
        Calculate the MACD value(s) for the given close prices.

        Parameters
            output_type : string, optional
                The types of output to return possible values are 'float' or 'numpy_array'. 
                If 'float', returns the MACD value as a float.
                If 'numpy_array', returns the MACD values as a numpy array of the same length as the input prices.
                Default is 'float'.

        Returns
            float or numpy.ndarray : The MACD value as a float if output_type is 'float', otherwise the MACD values as a 
                    numpy array.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """

        # Calculate the fast and slow EMAs
        fast_ema = MovingAverage(
            self.close_prices,
            self.fast_period).calculate_ema(output_type='numpy_array')

        slow_ema = MovingAverage(
            self.close_prices,
            self.slow_period).calculate_ema(output_type='numpy_array')

        # Calculate the MACD line
        if len(fast_ema) > len(slow_ema):
            fast_ema = fast_ema[-len(slow_ema):]
        elif len(slow_ema) > len(fast_ema):
            slow_ema = slow_ema[-len(fast_ema):]
        macd = fast_ema - slow_ema

        if output_type == 'float':
            return float(macd[-1])
        elif output_type == 'numpy_array':
            return macd
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )

    def calculate_signal_line(self, output_type='float'):
        """
        Calculate the Signal value(s) for the given close prices.

        Parameters
            output_type : string, optional
                The types of output to return possible values are 'float' or 'numpy_array'. 
                If 'float', returns the Signal value as a float.
                If 'numpy_array', returns the Signal values as a numpy array of the same length as the input prices.
                Default is 'float'.

        Returns
            float or numpy.ndarray : The Signal value as a float if output_type is 'float', otherwise the Signal values as a 
                    numpy array.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """

        # Calculate the MACD line
        macd = self.calculate_macd(output_type='numpy_array')

        # Calculate the signal line
        signal = MovingAverage(
            macd, self.signal_period).calculate_ema(output_type='numpy_array')

        if output_type == 'float':
            return float(signal[-1])
        elif output_type == 'numpy_array':
            return signal
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )
