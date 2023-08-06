import numpy as np


class OnBalanceVolume:

    def __init__(self, prices=[], volumes=[]):
        """
        Initializes an instance of the On Balance Volume (OBV) class.

        Args:
            prices (np.ndarray): array of close prices.
            volumes (np.ndarray): Array of volumes.
        """
        self.prices = np.asarray(prices)
        self.volumes = np.asarray(volumes)
        self.obv = np.zeros_like(prices)

    def calculate(self):
        """
        Calculates the OBV indicator for the initialized array of close prices and volumes.

        Returns:
            np.ndarray: Array of OBV values.
        """
        prev_obv = 0
        for i in range(1, len(self.prices)):
            if self.prices[i] > self.prices[i - 1]:
                self.obv[i] = prev_obv + self.volumes[i]
            elif self.prices[i] < self.prices[i - 1]:
                self.obv[i] = prev_obv - self.volumes[i]
            else:
                self.obv[i] = prev_obv
            prev_obv = self.obv[i]

        return self.obv
