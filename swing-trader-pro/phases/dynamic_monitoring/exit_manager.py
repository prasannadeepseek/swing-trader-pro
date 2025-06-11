# phases/3_dynamic_monitoring/exit_manager.py
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
