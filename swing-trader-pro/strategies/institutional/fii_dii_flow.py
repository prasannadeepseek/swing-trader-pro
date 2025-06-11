# strategies/institutional/fii_dii_flow.py
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
