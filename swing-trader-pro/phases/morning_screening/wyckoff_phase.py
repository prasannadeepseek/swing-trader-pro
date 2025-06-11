# phases/1_morning_screening/wyckoff_phase.py
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
