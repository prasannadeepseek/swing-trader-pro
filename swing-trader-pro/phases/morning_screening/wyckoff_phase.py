# phases/1_morning_screening/wyckoff_phase.py
from typing import Dict, Any, Sequence
import numpy as np


class WyckoffAnalyzer:
    def detect(self, price_data):
        """Detect Wyckoff accumulation/distribution phases"""
        closes = np.array(price_data['close'][-30:])
        volumes = np.array(price_data['volume'][-30:])

        # Simplified Wyckoff phase detection
        support = np.min(closes[-10:])
        resistance = np.max(closes[-10:])
        last_close = closes[-1]

        if (last_close > (support + resistance)/2 and
                volumes[-1] > np.mean(volumes[-5:])):
            return {
                'phase': 'accumulation',
                'score': 8,
                'support': support,
                'resistance': resistance
            }
        elif last_close < (support + resistance)/2:
            return {
                'phase': 'distribution',
                'score': 4,
                'support': support,
                'resistance': resistance
            }
        return {
            'phase': 'neutral',
            'score': 5,
            'support': support,
            'resistance': resistance
        }

# method 2 final version


class WyckoffAnalyzer:
    """
    Detects Wyckoff accumulation/distribution phases in price and volume data.
    """

    def __init__(self, window: int = 30, band: int = 10):
        """
        Args:
            window (int): Number of periods to consider for analysis.
            band (int): Number of periods for support/resistance calculation.
        """
        self.window = window
        self.band = band

    def detect(self, price_data: Dict[str, Sequence[float]]) -> Dict[str, Any]:
        """
        Detect Wyckoff accumulation/distribution/neutral phase.

        Args:
            price_data (dict): Dictionary with 'close' and 'volume' lists/arrays.

        Returns:
            dict: Phase info with keys: phase, score, support, resistance.
        """
        closes = np.array(price_data.get('close', []))
        volumes = np.array(price_data.get('volume', []))

        if len(closes) < self.window or len(volumes) < self.window:
            raise ValueError(
                f"Not enough data: need at least {self.window} closes and volumes.")

        closes = closes[-self.window:]
        volumes = volumes[-self.window:]

        support = np.min(closes[-self.band:])
        resistance = np.max(closes[-self.band:])
        last_close = closes[-1]

        # Defensive: avoid division by zero
        mean_recent_vol = np.mean(
            volumes[-min(5, len(volumes)):]) if len(volumes) >= 5 else np.mean(volumes)
        if mean_recent_vol == 0:
            mean_recent_vol = 1e-8

        if (last_close > (support + resistance) / 2 and
                volumes[-1] > mean_recent_vol):
            phase = 'accumulation'
            score = 8
        elif last_close < (support + resistance) / 2:
            phase = 'distribution'
            score = 4
        else:
            phase = 'neutral'
            score = 5

        return {
            'phase': phase,
            'score': score,
            'support': support,
            'resistance': resistance
        }
