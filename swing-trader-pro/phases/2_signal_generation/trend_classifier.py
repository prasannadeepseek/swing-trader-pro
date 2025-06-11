# phases/2_signal_generation/trend_classifier.py
import talib
import numpy as np
from collections import deque
# from swing_trader_pro.phases.morning_screening.wyckoff_phase import WyckoffAnalyzer
from phases.morning_screening.wyckoff_phase import WyckoffAnalyzer


class TrendClassifier:
    def __init__(self):
        self.trend_window = 20  # days
        self.confirmation_bars = 3

    def classify(self, symbol_data):
        """Classify trend with multiple confirmation methods"""
        closes = np.array(symbol_data['close'])
        volumes = np.array(symbol_data['volume'])

        # 1. Moving Average Analysis
        ma_status = self._ma_analysis(closes)

        # 2. Price Action Structure
        structure = self._price_structure(closes)

        # 3. Volume Confirmation
        volume_confirmation = self._volume_analysis(closes, volumes)

        # Composite classification
        if (ma_status == 'uptrend' and
            structure == 'higher_highs' and
                volume_confirmation):
            return 'uptrend'
        elif (ma_status == 'downtrend' and
              structure == 'lower_lows' and
              volume_confirmation):
            return 'downtrend'
        return 'neutral'

    def _ma_analysis(self, closes):
        """Analyze moving average crossovers"""
        sma20 = talib.SMA(closes, timeperiod=20)
        sma50 = talib.SMA(closes, timeperiod=50)

        if sma20[-1] > sma50[-1] and all(sma20[-self.confirmation_bars:] > sma50[-self.confirmation_bars:]):
            return 'uptrend'
        elif sma20[-1] < sma50[-1] and all(sma20[-self.confirmation_bars:] < sma50[-self.confirmation_bars:]):
            return 'downtrend'
        return 'neutral'

    def _price_structure(self, closes):
        """Analyze price structure for HH/HL or LH/LL"""
        peaks = []
        troughs = []

        for i in range(1, len(closes)-1):
            if closes[i] > closes[i-1] and closes[i] > closes[i+1]:
                peaks.append(closes[i])
            elif closes[i] < closes[i-1] and closes[i] < closes[i+1]:
                troughs.append(closes[i])

        if len(peaks) >= 2 and peaks[-1] > peaks[-2]:
            return 'higher_highs'
        elif len(troughs) >= 2 and troughs[-1] < troughs[-2]:
            return 'lower_lows'
        return 'neutral'

    def _volume_analysis(self, closes, volumes):
        """Confirm trends with volume"""
        price_change = closes[-1] / closes[-self.trend_window] - 1
        volume_change = volumes[-1] / np.mean(volumes[-self.trend_window:-1])

        if abs(price_change) > 0.05:  # 5% move
            return volume_change > 1.2  # 20% volume increase
        return True

# new code
# phases/2_signal_generation/trend_classifier.py


class TrendClassifier:
    def classify(self, symbol_data):
        """Classify trend using multiple technical factors"""
        closes = np.array(symbol_data['close'][-30:])

        # 1. Wyckoff Phase Detection
        wyckoff_phase = self.detect_wyckoff(closes)

        # 2. Moving Average Analysis
        ma_status = self.analyze_moving_averages(closes)

        # 3. Momentum Indicators
        momentum = self.calculate_momentum(closes)

        return {
            'symbol': symbol_data['symbol'],
            'wyckoff': wyckoff_phase,
            'ma_status': ma_status,
            'momentum': momentum,
            'composite_score': self.calculate_score(wyckoff_phase, ma_status, momentum)
        }

    def detect_wyckoff(self, closes):
        """Detect Wyckoff accumulation/distribution phases"""
        # Simplified implementation
        range_high = closes.max()
        range_low = closes.min()
        last_close = closes[-1]

        if last_close > (range_high + range_low) / 2:
            return {'phase': 'accumulation', 'score': 8}
        else:
            return {'phase': 'distribution', 'score': 4}

    def analyze_moving_averages(self, closes):
        """Analyze MA crossovers and slopes"""
        sma20 = talib.SMA(closes, timeperiod=20)
        sma50 = talib.SMA(closes, timeperiod=50)

        if sma20[-1] > sma50[-1] and sma20[-1] > sma20[-5]:
            return 'uptrend'
        elif sma20[-1] < sma50[-1] and sma20[-1] < sma20[-5]:
            return 'downtrend'
        return 'neutral'

    def calculate_momentum(self, closes):
        """Calculate composite momentum score"""
        rsi = talib.RSI(closes, timeperiod=14)[-1]
        macd, _, _ = talib.MACD(closes)
        macd_val = macd[-1] - macd[-2]

        if rsi > 60 and macd_val > 0:
            return 'strong'
        elif rsi < 40 and macd_val < 0:
            return 'weak'
        return 'neutral'

    def calculate_score(self, wyckoff, ma_status, momentum):
        """Calculate composite technical score"""
        score_map = {
            'uptrend': 8, 'downtrend': 3, 'neutral': 5,
            'strong': 7, 'weak': 2, 'neutral': 5
        }
        return (wyckoff['score'] * 0.5 +
                score_map[ma_status] * 0.3 +
                score_map[momentum] * 0.2)

# menthod 3


class SwingTrendClassifier:
    def classify(self, symbol_data):
        closes = symbol_data['close'][-30:]  # 30-day window

        # Wyckoff Phase Detection
        wyckoff_phase = WyckoffAnalyzer().detect(closes)

        # Quantitative Trend
        trend_strength = self._calculate_trend_strength(closes)

        return {
            'symbol': symbol_data['symbol'],
            'wyckoff_phase': wyckoff_phase,
            'trend_strength': trend_strength,
            'composite_score': 0.6*wyckoff_phase.score + 0.4*trend_strength
        }
