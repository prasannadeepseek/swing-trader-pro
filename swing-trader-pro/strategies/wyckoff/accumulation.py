# strategies/wyckoff/accumulation.py
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
