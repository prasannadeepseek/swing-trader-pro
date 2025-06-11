# strategies/wyckoff/distribution.py
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
