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
# method 3 best version
# core/risk_engine.py


class RiskEngine:
    """
    Unified RiskEngine for position sizing and risk validation,
    supporting both standard and institutional/hedge checks.
    """

    def calculate_position_size(self, entry, stop_loss, portfolio_value):
        """
        Calculate position size based on risk parameters.
        Returns the integer quantity to trade.
        """
        try:
            risk_amount = portfolio_value * constraints.MAX_RISK_PER_TRADE
            risk_per_share = abs(entry - stop_loss)
            if risk_per_share <= 0:
                raise ValueError(
                    "Invalid stop loss: entry and stop_loss must differ.")
            qty = int(risk_amount / risk_per_share)
            return max(qty, 0)
        except Exception as e:
            # Log error in production
            print(f"Error in position sizing: {e}")
            return 0

    def validate_trade(self, symbol_data):
        """
        Standard risk validation: volatility, liquidity, and max risk per trade.
        Returns True if all checks pass.
        """
        try:
            checks = [
                self._check_volatility(symbol_data),
                self._check_liquidity(symbol_data),
                self._check_max_risk(symbol_data)
            ]
            return all(checks)
        except Exception as e:
            print(f"Error in validate_trade: {e}")
            return False

    def validate_institutional_trade(self, symbol_data):
        """
        Enhanced validation for institutional trades, including hedge checks.
        Returns True if all checks pass.
        """
        try:
            # Basic checks
            if not (self._check_volatility(symbol_data) and self._check_liquidity(symbol_data)):
                return False

            # Hedge-specific checks
            fii_flows = symbol_data.get('fii_flows', {})
            net_cash = fii_flows.get('net_cash', 0)
            net_fno = fii_flows.get('net_fno', 1)  # Avoid division by zero

            if net_fno == 0:
                return False  # Cannot compute hedge ratio

            hedge_ratio = net_cash / abs(net_fno)
            delivery_pct = symbol_data.get('delivery_pct', 0)
            hedge_pct = symbol_data.get('hedge_pct', 0)
            delivery_gap = delivery_pct - hedge_pct

            return (
                hedge_ratio > hedge_constraints['cash_derivatives_ratio'] and
                delivery_gap > hedge_constraints['delivery_hedge_gap']
            )
        except Exception as e:
            print(f"Error in validate_institutional_trade: {e}")
            return False

    def _check_volatility(self, data):
        """Ensure volatility within acceptable range."""
        try:
            atr = data.get('atr', 0)
            close = data.get('close', 1)
            if close == 0:
                return False
            return (atr / close) < 0.1
        except Exception as e:
            print(f"Error in _check_volatility: {e}")
            return False

    def _check_liquidity(self, data):
        """Ensure sufficient trading volume."""
        try:
            avg_volume = data.get('avg_volume', 0)
            return avg_volume > 1e6
        except Exception as e:
            print(f"Error in _check_liquidity: {e}")
            return False

    def _check_max_risk(self, data):
        """Ensure risk per trade within limits."""
        try:
            entry = data.get('entry', 0)
            sl = data.get('sl', 0)
            if entry == 0:
                return False
            return (abs(entry - sl) / entry) < 0.05
        except Exception as e:
            print(f"Error in _check_max_risk: {e}")
            return False
