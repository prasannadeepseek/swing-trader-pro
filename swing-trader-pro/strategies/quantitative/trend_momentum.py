# strategies/quantitative/trend_momentum.py
from typing import Dict, Any, Optional
import numpy as np
import talib


class TrendMomentumStrategy:
    def analyze(self, data):
        """Identify trend momentum opportunities"""
        closes = data['close'][-50:]

        # Trend confirmation
        sma20 = talib.SMA(closes, timeperiod=20)[-1]
        sma50 = talib.SMA(closes, timeperiod=50)[-1]

        # Momentum confirmation
        rsi = talib.RSI(closes, timeperiod=14)[-1]
        macd, _, _ = talib.MACD(closes)

        if (sma20 > sma50 and
            rsi > 50 and
                macd[-1] > macd[-5]):
            return {
                'entry': closes[-1],
                'sl': min(closes[-20:]),
                'target': closes[-1] * 1.08,
                'score': 7
            }
        return None

# method 2 final version


class TrendMomentumStrategy:
    """
    Identifies trend momentum opportunities using SMA, RSI, and MACD.
    Generates long and short signals based on trend and momentum confirmation.
    """

    def analyze(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze price data for trend momentum signals.

        Args:
            data (dict): Must contain 'close' as a list or np.ndarray of recent closing prices.

        Returns:
            dict or None: Signal dictionary if a setup is detected, else None.
        """
        closes = np.asarray(data.get('close', []))
        if closes.size < 50:
            # Not enough data for 50-period indicators
            return None

        closes = closes[-50:]

        # Trend confirmation
        sma20 = talib.SMA(closes, timeperiod=20)[-1]
        sma50 = talib.SMA(closes, timeperiod=50)[-1]

        # Momentum confirmation
        rsi = talib.RSI(closes, timeperiod=14)[-1]
        macd, _, _ = talib.MACD(closes)

        # Long setup: uptrend, strong momentum
        if (sma20 > sma50 and rsi > 50 and macd[-1] > macd[-5]):
            return {
                'entry': closes[-1],
                'sl': float(np.min(closes[-20:])),
                'target': round(closes[-1] * 1.08, 2),
                'score': 7,
                'type': 'trend_momentum',
                'direction': 'long'
            }
        # Short setup: downtrend, weak momentum
        elif (sma20 < sma50 and rsi < 50 and macd[-1] < macd[-5]):
            return {
                'entry': closes[-1],
                'sl': float(np.max(closes[-20:])),
                'target': round(closes[-1] * 0.92, 2),
                'score': 6,
                'type': 'trend_momentum',
                'direction': 'short'
            }
        return None
