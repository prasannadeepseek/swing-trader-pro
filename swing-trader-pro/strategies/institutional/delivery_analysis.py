# strategies/institutional/delivery_analysis.py
from typing import Optional, Dict, Any


class DeliveryAnalysisStrategy:
    def analyze(self, data):
        """Analyze delivery volume patterns"""
        if data['delivery_pct'] > 40 and data['delivery_3day_avg'] > 1.5:
            return {
                'score': 8,
                'reason': 'high_delivery_volume',
                'validity_days': 2,
                'entry': data['close'],
                'sl': data['close'] * 0.97,
                'target': data['close'] * 1.06
            }
        elif data['delivery_pct'] < 25:
            return {
                'score': 3,
                'reason': 'low_delivery_volume',
                'validity_days': 1
            }
        return None
# method 2 final version
# strategies/institutional/delivery_analysis.py


class DeliveryAnalysisStrategy:
    """
    Analyzes delivery volume patterns to generate trading signals based on delivery percentage and averages.
    """

    def analyze(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze delivery volume patterns and return a signal dict if criteria are met.

        Args:
            data (dict): Must contain 'delivery_pct', 'delivery_3day_avg', and 'close' keys.

        Returns:
            dict or None: Signal dictionary if a pattern is detected, else None.
        """
        # Defensive: Ensure required keys exist and are valid numbers
        try:
            delivery_pct = float(data.get('delivery_pct', 0))
            delivery_3day_avg = float(data.get('delivery_3day_avg', 0))
            close = float(data.get('close', 0))
        except (TypeError, ValueError):
            return None

        if close <= 0:
            return None

        if delivery_pct > 40 and delivery_3day_avg > 1.5:
            return {
                'score': 8,
                'reason': 'high_delivery_volume',
                'validity_days': 2,
                'entry': close,
                'sl': round(close * 0.97, 2),
                'target': round(close * 1.06, 2)
            }
        elif delivery_pct < 25:
            return {
                'score': 3,
                'reason': 'low_delivery_volume',
                'validity_days': 1
            }
        return None
