# strategies/wyckoff/distribution.py
from phases.morning_screening.wyckoff_phase import WyckoffAnalyzer
from typing import Optional, Dict, Any
import phases.morning_screening.wyckoff_phase as WyckoffAnalyzer


class WyckoffDistributionStrategy:
    def analyze(self, price_data):
        """Detect distribution setups for short opportunities"""
        wyckoff = WyckoffAnalyzer().detect(price_data)

        if wyckoff['phase'] == 'distribution':
            return {
                'entry': wyckoff['support'] * 1.01,
                'sl': wyckoff['resistance'] * 1.02,
                'target': wyckoff['support'] * 0.94,
                'score': wyckoff['score'],
                'direction': 'short'
            }
        return None

# method 2 final version


class WyckoffDistributionStrategy:
    """
    Strategy to detect Wyckoff distribution setups and generate short trade signals.
    """

    def __init__(self, window: int = 30, band: int = 10):
        """
        Args:
            window (int): Number of periods for Wyckoff analysis.
            band (int): Number of periods for support/resistance calculation.
        """
        self.analyzer = WyckoffAnalyzer(window=window, band=band)

    def analyze(self, price_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Detect distribution setups using Wyckoff phase analysis.

        Args:
            price_data (dict): Must contain 'close' and 'volume' lists/arrays.

        Returns:
            dict or None: Trade signal dict if distribution detected, else None.
        """
        try:
            wyckoff = self.analyzer.detect(price_data)
        except Exception as e:
            # Log or handle error as needed
            print(
                f"[WyckoffDistributionStrategy] Error in Wyckoff analysis: {e}")
            return None

        if wyckoff.get('phase') == 'distribution':
            support = wyckoff.get('support')
            resistance = wyckoff.get('resistance')
            score = wyckoff.get('score', 0)
            if support is None or resistance is None:
                return None
            return {
                'entry': support * 1.01,
                'sl': resistance * 1.02,
                'target': support * 0.94,
                'score': score,
                'direction': 'short'
            }
        return None
