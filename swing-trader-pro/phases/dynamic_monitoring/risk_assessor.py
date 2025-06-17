from typing import Dict
from volume.analysis import VolumeAnalysis
from technicals.analysis import Technicals
from data.institutional import InstitutionalData
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

# method 2 final version


class SwingRiskAssessor:
    """
    Assesses risk for a given symbol based on institutional activity, technicals, and volume.
    Returns a capped risk score and recommended action.
    """

    MAX_SCORE = 10

    def evaluate(self, symbol: str) -> Dict[str, object]:
        """
        Evaluate the risk for a trading symbol.

        Args:
            symbol (str): The trading symbol.

        Returns:
            dict: {
                'symbol': str,
                'risk_score': int,
                'action': str
            }
        """
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

        risk_score = min(risk_score, self.MAX_SCORE)
        action = self._determine_action(risk_score)

        return {
            'symbol': symbol,
            'risk_score': risk_score,
            'action': action
        }

    def _determine_action(self, score: int) -> str:
        """
        Map risk score to recommended action.

        Args:
            score (int): The risk score.

        Returns:
            str: Action recommendation.
        """
        if score >= 7:
            return 'emergency_exit'
        elif score >= 4:
            return 'partial_exit'
        else:
            return 'hold'
