# core/risk_engine.py
# from config.constraints import MAX_RISK_PER_TRADE
from config import hedge_constraints
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

# method 2
# core/risk_engine.py


class RiskEngine:
    def validate_institutional_trade(self, symbol_data):
        """Enhanced validation with hedge checks"""
        basic_checks = (
            self._check_volatility(symbol_data) and
            self._check_liquidity(symbol_data)
        )

        if not basic_checks:
            return False

        # Hedge-specific checks
        hedge_ratio = symbol_data['fii_flows']['net_cash'] / \
            abs(symbol_data['fii_flows']['net_fno'])
        delivery_gap = symbol_data['delivery_pct'] - symbol_data['hedge_pct']

        return (
            hedge_ratio > hedge_constraints['cash_derivatives_ratio'] and
            delivery_gap > hedge_constraints['delivery_hedge_gap']
        )
