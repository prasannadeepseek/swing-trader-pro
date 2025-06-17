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


class TrendClassifier:
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

# method 4 final version


class TrendClassifier:
    """
    Unified TrendClassifier combining Wyckoff, moving averages, price structure,
    volume confirmation, and momentum for robust trend detection and scoring.
    """

    def __init__(self, trend_window=20, confirmation_bars=3):
        self.trend_window = trend_window
        self.confirmation_bars = confirmation_bars
        self.wyckoff_analyzer = WyckoffAnalyzer()

    def classify(self, symbol_data):
        """
        Classify trend using multiple technical factors and return a rich result dict.
        """
        closes = np.array(symbol_data['close'][-max(50, self.trend_window):])
        volumes = np.array(symbol_data['volume'][-max(50, self.trend_window):])
        symbol = symbol_data.get('symbol', 'UNKNOWN')

        if len(closes) < 50 or len(volumes) < 20:
            return {
                'symbol': symbol,
                'error': 'Insufficient data for trend classification',
                'composite_score': 0,
                'details': {}
            }

        # 1. Wyckoff Phase Detection (external analyzer)
        wyckoff_result = self.wyckoff_analyzer.detect({
            'close': closes,
            'volume': volumes
        })
        wyckoff_phase = wyckoff_result.get('phase', 'neutral')
        wyckoff_score = wyckoff_result.get('score', 5)

        # 2. Moving Average Analysis
        ma_status = self._ma_analysis(closes)
        ma_score = {'uptrend': 8, 'downtrend': 3, 'neutral': 5}[ma_status]

        # 3. Price Structure
        structure = self._price_structure(closes)
        structure_score = {'higher_highs': 8,
                           'lower_lows': 3, 'neutral': 5}[structure]

        # 4. Volume Confirmation
        volume_confirmation = self._volume_analysis(closes, volumes)
        volume_score = 8 if volume_confirmation else 3

        # 5. Momentum (RSI, MACD)
        momentum = self._momentum(closes)
        momentum_score = {'strong': 8, 'weak': 3, 'neutral': 5}[momentum]

        # Composite score (weighted)
        composite_score = (
            0.3 * wyckoff_score +
            0.2 * ma_score +
            0.15 * structure_score +
            0.15 * volume_score +
            0.2 * momentum_score
        )

        return {
            'symbol': symbol,
            'wyckoff_phase': wyckoff_phase,
            'wyckoff_score': wyckoff_score,
            'ma_status': ma_status,
            'structure': structure,
            'volume_confirmation': volume_confirmation,
            'momentum': momentum,
            'composite_score': round(composite_score, 2),
            'details': {
                'ma_score': ma_score,
                'structure_score': structure_score,
                'volume_score': volume_score,
                'momentum_score': momentum_score
            }
        }

    def _ma_analysis(self, closes):
        """Analyze moving average crossovers and confirmation bars."""
        sma20 = talib.SMA(closes, timeperiod=20)
        sma50 = talib.SMA(closes, timeperiod=50)
        if len(sma20) < self.confirmation_bars or len(sma50) < self.confirmation_bars:
            return 'neutral'
        if (
            sma20[-1] > sma50[-1] and
            all(sma20[-self.confirmation_bars:] >
                sma50[-self.confirmation_bars:])
        ):
            return 'uptrend'
        elif (
            sma20[-1] < sma50[-1] and
            all(sma20[-self.confirmation_bars:] <
                sma50[-self.confirmation_bars:])
        ):
            return 'downtrend'
        return 'neutral'

    def _price_structure(self, closes):
        """Analyze price structure for higher highs/lows or lower highs/lows."""
        peaks, troughs = [], []
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
        """Confirm trends with volume."""
        if len(closes) < self.trend_window or len(volumes) < self.trend_window:
            return False
        price_change = closes[-1] / closes[-self.trend_window] - 1
        volume_change = volumes[-1] / np.mean(volumes[-self.trend_window:-1])
        if abs(price_change) > 0.05:  # 5% move
            return volume_change > 1.2  # 20% volume increase
        return True

    def _momentum(self, closes):
        """Calculate composite momentum using RSI and MACD."""
        rsi = talib.RSI(closes, timeperiod=14)[-1]
        macd, _, _ = talib.MACD(closes)
        macd_val = macd[-1] - macd[-2]
        if rsi > 60 and macd_val > 0:
            return 'strong'
        elif rsi < 40 and macd_val < 0:
            return 'weak'
        return 'neutral'
