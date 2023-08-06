import numpy as np
from typing import List, Union


class MovingAverage:
    """
    A class used to calculate Moving Average indicators.

    Attributes
        close_prices : Union[List[float], np.ndarray]
            A list or numpy array of close prices for the asset.
        period : int, optional
            The number of time periods used for the Moving Average indicator calculation.

    Methods
        calculate_sma(output_type='float') : Union[float, np.ndarray]
            Calculate the Simple Moving Average (SMA) value(s) for the given close prices.
        calculate_ema(output_type='float') : Union[float, np.ndarray]
            Calculate the Exponential Moving Average (EMA) value(s) for the given close prices.
        calculate_wma(output_type='float') : Union[float, np.ndarray]
            Calculate the Weighted Moving Average (WMA) value(s) for the given close prices.
        calculate_hma(output_type='float') : Union[float, np.ndarray]
            Calculate the Hull Moving Average (HMA) value(s) for the given close prices.
    """

    def __init__(self, close_prices=[], period=9):
        """
        Constructor for the MovingAverage class.

        Parameters
            close_prices : Union[List[float], np.ndarray]
                List or numpy array of close prices for the asset.
            period : int, optional
                The number of periods used to calculate the moving average. Default is 9.
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

    def calculate_sma(self, output_type='float'):
        """
        Calculate the Simple Moving Average (SMA) of the given close prices.

        Parameters
            output_type : string, optional
                The types of output to return possible values are 'float' or 'numpy_array'. 
                If 'float', returns the SMA value as a float.
                If 'numpy_array', returns the SMA values as a numpy array of the same length as the input prices.
                Default is 'float'.

        Returns
            float or numpy.ndarray : The SMA value as a float if output_type is 'float', otherwise the SMA values as a 
                                numpy array.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """
        # Initialize the output list
        sma = []

        # Loop over the close prices to calculate the SMA
        for i in range(len(self.close_prices)):
            if i < self.period - 1:
                # If there are not enough elements to fill the window, use the available ones
                window = self.close_prices[:i + 1]
            else:
                # Otherwise, use the last 'period' elements
                window = self.close_prices[i - self.period + 1:i + 1]

            # Calculate the SMA and append it to the output list
            sma_item = np.mean(window)
            sma.append(sma_item)

        # Create a numpy array from the list of SMA
        sma = np.array(sma)

        # Return result in the desired output format
        if output_type == 'float':
            return sma[-1]
        elif output_type == 'numpy_array':
            return sma
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )

    def calculate_ema(self, output_type='float'):
        """
        Calculate the Exponential Moving Average (EMA) of the given close prices.

        Parameters
            output_type : string, optional
                The types of output to return possible values are 'float' or 'numpy_array'. 
                If 'float', returns the EMA value as a float.
                If 'numpy_array', returns the EMA values as a numpy array of the same length as the input prices.
                Default is 'float'.

        Returns
            float or numpy.ndarray : The EMA value as a float if output_type is 'float', otherwise the EMA values as a 
                                numpy array.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """
        # Initialize the output list
        ema = []

        # Calculate the smoothing factor
        smoothing_factor = 2 / (self.period + 1)

        # Calculate the initial EMA
        ema_item = self.close_prices[0]
        ema.append(ema_item)

        # Loop over the remaining close prices to calculate the EMA
        for price in self.close_prices[1:]:
            ema_item = (price * smoothing_factor) + (ema_item *
                                                     (1 - smoothing_factor))
            ema.append(ema_item)

        # Create a numpy array from the list of EMA
        ema = np.array(ema)

        # Return result in the desired output format
        if output_type == 'float':
            return ema[-1]
        elif output_type == 'numpy_array':
            return ema
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )

    def calculate_wma(self, output_type='float'):
        """
        Calculate the WMA (Weighted Moving Average) for the given close prices.
        
        Parameters
            output_type : string, optional
                The type of output to return. Can be 'float' or 'numpy_array'. Default is 'float'.
        
        Returns

            Union[float, np.ndarray]
                The WMA value(s) for the given close prices.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """
        weights = np.arange(1, self.period + 1, dtype=float)
        wma_values = np.zeros_like(self.close_prices, dtype=float)

        for i in range(self.period - 1, len(self.close_prices)):
            wma_values[i] = np.sum(
                weights *
                self.close_prices[i - self.period + 1:i + 1]) / np.sum(weights)

        # Return the output based on the specified output_type
        if output_type == 'float':
            return float(wma_values[-1])
        elif output_type == 'numpy_array':
            return wma_values
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )

    def calculate_hma(self, output_type='float'):
        """
        Calculate the HMA (Hull Moving Average) for the given close prices.
        
        Parameters

            output_type : string, optional
                The type of output to return. Can be 'float' or 'numpy_array'. Default is 'float'.
        
        Returns

            Union[float, np.ndarray]
                The HMA value(s) for the given close prices.

        Raises
            ValueError : If output_type is not 'float' or 'numpy_array'.
        """
        wma_half_period = np.zeros(len(self.close_prices))
        for i in range(self.period, len(self.close_prices)):
            wma_period = int(np.round(np.sqrt(self.period)))
            weights = np.arange(1, wma_period + 1)
            wma_weights = weights / weights.sum()

            # Calculate the first WMA
            wma_values1 = np.convolve(self.close_prices[i - wma_period:i +
                                                        wma_period + 1],
                                      wma_weights,
                                      mode='valid')

            # Calculate the second WMA
            wma_period2 = int(np.round(np.sqrt(wma_period)))
            weights2 = np.arange(1, wma_period2 + 1)
            wma_weights2 = weights2 / weights2.sum()
            wma_values2 = np.convolve(self.close_prices[i - wma_period2:i +
                                                        wma_period2 + 1],
                                      wma_weights2,
                                      mode='valid')

            # Calculate the HMA value
            wma_half_period[i] = 2 * wma_values1[-1] - wma_values2[-1]

        hma_period = int(np.round(np.sqrt(self.period)))
        weights = np.arange(1, hma_period + 1)
        hma_weights = weights / weights.sum()
        hma_values = np.convolve(wma_half_period, hma_weights, mode='valid')

        # Return the output based on the specified output_type
        if output_type == 'float':
            return float(hma_values[-1])
        elif output_type == 'numpy_array':
            return hma_values
        else:
            raise ValueError(
                f"Invalid output type '{output_type}'. Valid values are 'float' or 'numpy_array'."
            )
