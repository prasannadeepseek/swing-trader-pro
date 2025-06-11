# core/risk_engine.py
# from config.constraints import MAX_RISK_PER_TRADE
from config import constraints


class RiskEngine:
    def calculate_position_size(self, entry, stop_loss, portfolio_value):
        """Calculate quantity based on risk parameters"""
        risk_amount = portfolio_value * constraints.MAX_RISK_PER_TRADE
        risk_per_share = entry - stop_loss
        return int(risk_amount / risk_per_share)

    def validate_trade(self, symbol_data):
        """Check if trade meets all risk criteria"""
        checks = [
            self._check_volatility(symbol_data),
            self._check_liquidity(symbol_data),
            self._check_max_risk(symbol_data)
        ]
        return all(checks)

    def _check_volatility(self, data):
        """Ensure volatility within acceptable range"""
        return data['atr'] / data['close'] < 0.1

    def _check_liquidity(self, data):
        """Ensure sufficient trading volume"""
        return data['avg_volume'] > 1e6

    def _check_max_risk(self, data):
        """Ensure risk per trade within limits"""
        return (data['entry'] - data['sl']) / data['entry'] < 0.05
