# strategies/quantitative/mean_reversion.py
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
