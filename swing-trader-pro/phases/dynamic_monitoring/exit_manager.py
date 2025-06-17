# phases/3_dynamic_monitoring/exit_manager.py
from typing import Dict, Any, List, Optional
from core.risk_engine import RiskEngine


class ExitManager:
    def __init__(self):
        self.risk_engine = RiskEngine()

    def evaluate_exits(self, positions):
        """Determine which positions should be exited"""
        exits = []

        for symbol, position in positions.items():
            exit_reason = self._check_exit_conditions(position)
            if exit_reason:
                exits.append({
                    'symbol': symbol,
                    'reason': exit_reason,
                    'quantity': position['quantity']
                })

        return exits

    def _check_exit_conditions(self, position):
        """Check all exit conditions for a position"""
        if position['pnl_pct'] <= -position['sl_pct']:
            return 'stop_loss_triggered'
        elif position['pnl_pct'] >= position['target_pct']:
            return 'target_achieved'
        elif self.risk_engine.check_emergency_exit(position):
            return 'risk_emergency'
        return None

# method 3 final version


class ExitManager:
    """
    Manages exit logic for open trading positions, including stop loss, target, and risk-based exits.
    """

    def __init__(self):
        self.risk_engine = RiskEngine()

    def evaluate_exits(self, positions: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Determine which positions should be exited.

        Args:
            positions (dict): Mapping of symbol to position dict.

        Returns:
            List[dict]: List of exit instructions with symbol, reason, and quantity.
        """
        exits = []
        for symbol, position in positions.items():
            exit_reason = self.evaluate_single_exit(position)
            if exit_reason:
                exits.append({
                    'symbol': symbol,
                    'reason': exit_reason,
                    'quantity': position.get('quantity', 0)
                })
        return exits

    def evaluate_single_exit(self, position: Dict[str, Any]) -> Optional[str]:
        """
        Evaluate exit conditions for a single position.

        Args:
            position (dict): Position data.

        Returns:
            str or None: Reason for exit, or None if no exit triggered.
        """
        pnl_pct = position.get('pnl_pct')
        sl_pct = position.get('sl_pct')
        target_pct = position.get('target_pct')

        # Defensive: Ensure required keys exist and are numbers
        if pnl_pct is None or sl_pct is None or target_pct is None:
            return None

        if pnl_pct <= -sl_pct:
            return 'stop_loss_triggered'
        elif pnl_pct >= target_pct:
            return 'target_achieved'
        elif hasattr(self.risk_engine, "check_emergency_exit") and self.risk_engine.check_emergency_exit(position):
            return 'risk_emergency'
        return None
