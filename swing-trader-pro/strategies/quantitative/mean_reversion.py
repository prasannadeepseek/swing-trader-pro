# strategies/quantitative/mean_reversion.py
from typing import Dict, Any, Optional
import talib
import numpy as np


class MeanReversionStrategy:
    def analyze(self, data):
        """Identify mean reversion opportunities"""
        closes = np.array(data['close'][-20:])
        upper, middle, lower = talib.BBANDS(closes, timeperiod=20)

        rsi = talib.RSI(closes, timeperiod=14)[-1]

        if closes[-1] < lower[-1] and rsi < 35:
            return {
                'entry': closes[-1],
                'sl': closes[-1] * 0.96,
                'target': middle[-1],
                'score': 7,
                'type': 'mean_reversion'
            }
        elif closes[-1] > upper[-1] and rsi > 65:
            return {
                'entry': closes[-1],
                'sl': closes[-1] * 1.04,
                'target': middle[-1],
                'score': 6,
                'type': 'mean_reversion',
                'direction': 'short'
            }
        return None

# method 2 final version


class MeanReversionStrategy:
    """
    Identifies mean reversion opportunities using Bollinger Bands and RSI.
    Generates long and short signals based on price and momentum extremes.
    """

    def analyze(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze price data for mean reversion signals.

        Args:
            data (dict): Must contain 'close' as a list or np.ndarray of recent closing prices.

        Returns:
            dict or None: Signal dictionary if a setup is detected, else None.
        """
        closes = np.asarray(data.get('close', []))
        if closes.size < 20:
            # Not enough data for 20-period indicators
            return None

        # Calculate Bollinger Bands and RSI
        upper, middle, lower = talib.BBANDS(closes, timeperiod=20)
        rsi = talib.RSI(closes, timeperiod=14)[-1]

        last_close = closes[-1]
        signal = None

        # Long setup: price below lower band and oversold RSI
        if last_close < lower[-1] and rsi < 35:
            signal = {
                'entry': last_close,
                'sl': round(last_close * 0.96, 2),
                'target': round(middle[-1], 2),
                'score': 7,
                'type': 'mean_reversion',
                'direction': 'long'
            }
        # Short setup: price above upper band and overbought RSI
        elif last_close > upper[-1] and rsi > 65:
            signal = {
                'entry': last_close,
                'sl': round(last_close * 1.04, 2),
                'target': round(middle[-1], 2),
                'score': 6,
                'type': 'mean_reversion',
                'direction': 'short'
            }

        return signal
