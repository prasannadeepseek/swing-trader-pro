# strategies/institutional/hedge_detector.py
import numpy as np
from config import hedge_constraints


class HedgeDetector:
    def __init__(self):
        self.constraints = hedge_constraints

    def detect_hedges(self, symbol, fii_data, oi_data):
        """Main detection method"""
        return {
            'index_hedge': self._check_index_hedge(fii_data, oi_data),
            'sector_hedge': self._check_sector_hedge(symbol, fii_data),
            'pair_trade': self._check_pair_trade(symbol)
        }

    def _check_index_hedge(self, fii_data, oi_data):
        cash_ratio = fii_data['net_cash'] / abs(fii_data['net_fno'])
        oi_change = oi_data['nifty_oi_pct_change']
        return (cash_ratio < self.constraints['cash_derivatives_ratio']
                and oi_change > self.constraints['index_oi_change_limit'])

    def _check_sector_hedge(self, symbol, fii_data):
        sector_flow = self._get_sector_flow(symbol)
        return sector_flow < self.constraints['sector_flow_threshold']

    def _get_sector_flow(self, symbol):
        # Implementation would fetch sector ETF flows
        return -3.2e7  # Mock value
