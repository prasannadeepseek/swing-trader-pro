from data.institutional import InstitutionalData  # Need to create this
from technicals.analysis import Technicals  # Need to create this
from volume.analysis import VolumeAnalysis  # Need to create this


class SwingRiskAssessor:
    def evaluate(self, symbol):
        risk_score = 0

        # 1. Institutional outflow
        if InstitutionalData.recent_selling(symbol):
            risk_score += 3

        # 2. Technical breakdown
        if Technicals.support_break(symbol):
            risk_score += 4

        # 3. Volume drying up
        if VolumeAnalysis.is_drying(symbol):
            risk_score += 2

        return {
            'symbol': symbol,
            'risk_score': min(risk_score, 10),
            'action': self._determine_action(risk_score)
        }

    def _determine_action(self, score):
        if score >= 7:
            return 'emergency_exit'
        elif score >= 4:
            return 'partial_exit'
        else:
            return 'hold'
