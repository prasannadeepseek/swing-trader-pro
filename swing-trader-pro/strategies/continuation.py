# strategies/continuation.py
import pandas as pd
import numpy as np


class ContinuationSignalChecker:
    def evaluate(self, symbol):
        # Implement your continuation signal logic
        return {
            'update_sl': False,
            'new_sl': 0,
            'new_target': 0,
            'sl_change_pct': 0,
            'target_change_pct': 0
        }
# method 2 final version
# strategies/continuation.py


class ContinuationSignalChecker:
    """
    Checks for continuation signals using price and indicator data.
    Extend this class to implement more sophisticated logic.
    """

    def __init__(self, data_provider=None):
        """
        Args:
            data_provider (callable, optional): Function to fetch historical price data for a symbol.
                Should accept a symbol and return a DataFrame with 'close' prices.
        """
        self.data_provider = data_provider or self._default_data_provider

    def evaluate(self, symbol):
        """
        Evaluate whether a continuation signal is present for the given symbol.

        Args:
            symbol (str): The trading symbol.

        Returns:
            dict: {
                'update_sl': bool,
                'new_sl': float,
                'new_target': float,
                'sl_change_pct': float,
                'target_change_pct': float
            }
        """
        # Fetch historical data
        df = self.data_provider(symbol)
        if df is None or len(df) < 21:
            # Not enough data, return default
            return {
                'update_sl': False,
                'new_sl': 0,
                'new_target': 0,
                'sl_change_pct': 0,
                'target_change_pct': 0
            }

        # Example logic: If price is above 20-period SMA, suggest trailing SL up
        close = df['close'].values
        sma20 = pd.Series(close).rolling(window=20).mean().values
        last_close = close[-1]
        last_sma20 = sma20[-1]

        update_sl = False
        new_sl = 0
        new_target = 0
        sl_change_pct = 0
        target_change_pct = 0

        if last_close > last_sma20:
            # Suggest trailing stop-loss to just below SMA
            update_sl = True
            new_sl = round(last_sma20 * 0.995, 2)
            new_target = round(last_close * 1.04, 2)
            sl_change_pct = (new_sl - close[-2]) / \
                close[-2] if close[-2] != 0 else 0
            target_change_pct = 0.04

        return {
            'update_sl': update_sl,
            'new_sl': new_sl,
            'new_target': new_target,
            'sl_change_pct': sl_change_pct,
            'target_change_pct': target_change_pct
        }

    def _default_data_provider(self, symbol):
        """
        Placeholder for fetching historical price data.
        Replace with actual data fetching logic.
        """
        # Example: Return None to indicate no data
        return None
