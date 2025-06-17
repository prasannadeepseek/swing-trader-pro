# strategies/institutional/fii_dii_flow.py
from typing import Optional, Dict, Any
from .hedge_detector import HedgeDetector
from config import constraints, hedge_constraints


class InstitutionalStrategy:
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

# method 3 final version


class InstitutionalStrategy:
    """
    InstitutionalStrategy generates trading signals based on institutional flows (FII/DII)
    and optionally adjusts for hedging activity using HedgeDetector.
    """

    def __init__(self, use_hedge_detection: bool = True):
        """
        Args:
            use_hedge_detection (bool): If True, use hedge detection logic; else use simple flow logic.
        """
        self.use_hedge_detection = use_hedge_detection
        self.hedge_detector = HedgeDetector() if use_hedge_detection else None
        self.min_net_buy = constraints['CAP_THRESHOLDS']['large']

    def analyze(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze institutional data and generate a trading signal.

        Args:
            data (dict): Symbol data. For hedge detection, must include:
                - 'symbol'
                - 'close'
                - 'fii_flows' (dict with 'net_3day', etc.)
                - 'oi_changes' (dict)
            For simple mode, must include:
                - 'fii_net'
                - 'dii_net'

        Returns:
            dict or None: Signal dictionary if criteria met, else None.
        """
        if self.use_hedge_detection:
            # Defensive: Ensure required keys exist
            if not all(k in data for k in ('symbol', 'close', 'fii_flows', 'oi_changes')):
                return None

            fii_data = data['fii_flows']
            oi_data = data['oi_changes']

            # Defensive: Check for required FII data
            if 'net_3day' not in fii_data or fii_data['net_3day'] is None:
                return None

            if fii_data['net_3day'] < self.min_net_buy:
                return None

            hedge_flags = self.hedge_detector.detect_hedges(
                data['symbol'],
                fii_data,
                oi_data
            )
            return self._generate_signal(data, hedge_flags)
        else:
            # Simple mode: only FII/DII net flows
            if 'fii_net' not in data or 'dii_net' not in data:
                return None

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

    def _generate_signal(self, data: Dict[str, Any], hedge_flags: Dict[str, bool]) -> Dict[str, Any]:
        """
        Generate a trade signal, adjusting for hedge detection.

        Args:
            data (dict): Symbol data.
            hedge_flags (dict): Output from HedgeDetector.detect_hedges().

        Returns:
            dict: Signal dictionary.
        """
        base_signal = {
            'symbol': data['symbol'],
            'entry': data['close'],
            'sl': round(data['close'] * 0.9, 2),
            'target': round(data['close'] * 1.1, 2),
            'score': 8  # Base score
        }

        if any(hedge_flags.values()):
            base_signal['score'] -= 3
            base_signal['weight'] = 0.5  # Reduce position weight
            base_signal['reason'] = 'hedged_flow'
        else:
            base_signal['weight'] = 1.0
            base_signal['reason'] = 'pure_accumulation'

        return base_signal
