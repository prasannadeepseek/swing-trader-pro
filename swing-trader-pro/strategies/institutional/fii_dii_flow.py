# strategies/institutional/fii_dii_flow.py
from .hedge_detector import HedgeDetector
from config import constraints, hedge_constraints


class InstitutionalFlowStrategy:
    def analyze(self, data):
        """Generate signals based on institutional flows"""
        if data['fii_net'] > 2e7 and data['dii_net'] > 1e7:
            return {
                'score': 9,
                'reason': 'strong_institutional_inflow',
                'validity_days': 3
            }
        elif data['fii_net'] < -1e7:
            return {
                'score': 2,
                'reason': 'fii_selling',
                'validity_days': 1
            }
        return None

# method 2
# strategies/institutional/fii_dii_flow.py


class InstitutionalStrategy:
    def __init__(self):
        self.hedge_detector = HedgeDetector()
        self.min_net_buy = constraints['CAP_THRESHOLDS']['large']

    def analyze(self, symbol_data):
        """Enhanced analysis with hedge detection"""
        fii_data = symbol_data['fii_flows']
        oi_data = symbol_data['oi_changes']

        # Basic FII check
        if fii_data['net_3day'] < self.min_net_buy:
            return None

        # Hedge detection
        hedge_flags = self.hedge_detector.detect_hedges(
            symbol_data['symbol'],
            fii_data,
            oi_data
        )

        # Adjust signal based on hedges
        return self._generate_signal(symbol_data, hedge_flags)

    def _generate_signal(self, data, hedge_flags):
        """Generate trade signal with hedge adjustments"""
        base_signal = {
            'symbol': data['symbol'],
            'entry': data['close'],
            'sl': data['close'] * 0.9,
            'target': data['close'] * 1.1,
            'score': 8  # Base score
        }

        # Penalize for hedging activities
        if any(hedge_flags.values()):
            base_signal['score'] -= 3
            base_signal['weight'] = 0.5  # Reduce position weight
            base_signal['reason'] = 'hedged_flow'
        else:
            base_signal['weight'] = 1.0
            base_signal['reason'] = 'pure_accumulation'

        return base_signal
