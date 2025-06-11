# strategies/quantitative/trend_momentum.py
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
