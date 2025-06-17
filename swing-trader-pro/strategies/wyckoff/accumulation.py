# strategies/wyckoff/accumulation.py
from typing import Optional, Dict, Any
from phases.morning_screening.wyckoff_phase import WyckoffAnalyzer


class WyckoffAccumulationStrategy:
    def analyze(self, price_data):
        """Detect accumulation setups"""
        wyckoff = WyckoffAnalyzer().detect(price_data)

        if wyckoff['phase'] == 'accumulation':
            return {
                'entry': wyckoff['resistance'] * 0.99,
                'sl': wyckoff['support'] * 0.98,
                'target': wyckoff['resistance'] * 1.1,
                'score': wyckoff['score']
            }
        return None
# method 2 final version
# strategies/wyckoff/accumulation.py


class WyckoffAccumulationStrategy:
    """
    Strategy to detect Wyckoff accumulation setups and generate trade signals.
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
        Detect accumulation setups using Wyckoff phase analysis.

        Args:
            price_data (dict): Must contain 'close' and 'volume' lists/arrays.

        Returns:
            dict or None: Trade signal dict if accumulation detected, else None.
        """
        try:
            wyckoff = self.analyzer.detect(price_data)
        except Exception as e:
            # Log or handle error as needed
            print(
                f"[WyckoffAccumulationStrategy] Error in Wyckoff analysis: {e}")
            return None

        if wyckoff.get('phase') == 'accumulation':
            resistance = wyckoff.get('resistance')
            support = wyckoff.get('support')
            score = wyckoff.get('score', 0)
            if resistance is None or support is None:
                return None
            return {
                'entry': resistance * 0.99,
                'sl': support * 0.98,
                'target': resistance * 1.1,
                'score': score
            }
        return None
