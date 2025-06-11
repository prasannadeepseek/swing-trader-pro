# strategies/institutional/delivery_analysis.py
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
