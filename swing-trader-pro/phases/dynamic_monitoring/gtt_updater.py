# phases/3_dynamic_monitoring/gtt_updater.py
from core.position_manager import active_positions
from typing import List, Dict, Any
import random
from brokers.zerodha import ZerodhaAdapter
from core.position_manager import active_positions  # Need to create this
from strategies.continuation import ContinuationSignalChecker
from brokers.broker_adapter import BrokerAdapter
from alerts.telegram import TelegramAlerts


class GTTManager:
    def __init__(self):
        self.broker = ZerodhaAdapter()
        self.checks_today = self.generate_check_schedule()

    def run_checks(self):
        """Execute scheduled GTT checks"""
        for symbol in self.get_active_positions():
            self.check_position(symbol)

    def check_position(self, symbol):
        """Check if GTT needs update for a position"""
        analysis = self.analyze_position(symbol)

        if analysis['update_needed']:
            self.broker.modify_gtt(
                symbol=symbol,
                new_sl=analysis['new_sl'],
                new_target=analysis['new_target']
            )

    def analyze_position(self, symbol):
        """Determine if GTT should be updated"""
        price_data = self.get_price_data(symbol)
        current_pnl = self.calculate_pnl(symbol)

        # Example update logic
        if current_pnl > 0.03:  # 3% profit
            return {
                'update_needed': True,
                # Trail to 1% below current
                'new_sl': price_data['current'] * 0.99,
                'new_target': price_data['current'] * 1.05  # New 5% target
            }
        return {'update_needed': False}

    def generate_check_schedule(self):
        """Generate random check times (2-4 between 9:15-15:15)"""
        return sorted([
            f"{random.randint(9, 14)}:{random.randint(15, 45):02d}"
            for _ in range(random.randint(2, 4))
        ])
# metod 2


class GTTManager:
    def __init__(self):
        self.check_schedule = self._generate_schedule()

    def run_check(self):
        for symbol in active_positions:
            # 1. Check continuation signals
            signal = ContinuationSignalChecker().evaluate(symbol)

            # 2. Update orders if needed
            if signal['update_sl']:
                BrokerAdapter().modify_gtt(
                    symbol=symbol,
                    new_sl=signal['new_sl'],
                    new_target=signal['new_target']
                )

                # Alert
                TelegramAlerts.gtt_update(
                    symbol=symbol,
                    sl_change=signal['sl_change_pct'],
                    target_change=signal['target_change_pct']
                )

    def _generate_schedule(self):
        # 2-4 random checks between 9:15-15:15
        return sorted(random.sample(
            range(9*60+15, 15*60+15),
            random.randint(2, 4)
        ))

# method 3 final version


class GTTManager:
    """
    Manages scheduled checks and updates for GTT orders based on position signals and PnL.
    """

    def __init__(self, broker_name: str = "zerodha"):
        """
        Args:
            broker_name (str): The broker to use for GTT management.
        """
        self.broker = BrokerAdapter(broker=broker_name)
        self.check_schedule = self._generate_schedule()
        self.signal_checker = ContinuationSignalChecker()

    def run_checks(self):
        """
        Execute scheduled GTT checks for all active positions.
        """
        for symbol in self.get_active_positions():
            self.check_position(symbol)

    def check_position(self, symbol: str):
        """
        Check if a GTT order needs to be updated for a given position.

        Args:
            symbol (str): The trading symbol.
        """
        # 1. Evaluate continuation signal
        signal = self.signal_checker.evaluate(symbol)

        # 2. Optionally, add PnL-based logic (example)
        current_pnl = self.calculate_pnl(symbol)
        price_data = self.get_price_data(symbol)
        update_needed = signal.get('update_sl', False)

        # Example: If PnL > 3%, trail SL and raise target
        if current_pnl is not None and current_pnl > 0.03:
            update_needed = True
            signal['new_sl'] = price_data['current'] * 0.99
            signal['new_target'] = price_data['current'] * 1.05
            signal['sl_change_pct'] = -0.01
            signal['target_change_pct'] = 0.05

        if update_needed:
            self.broker.modify_gtt(
                symbol=symbol,
                new_sl=signal['new_sl'],
                new_target=signal['new_target']
            )
            TelegramAlerts.gtt_update(
                symbol=symbol,
                sl_change=signal.get('sl_change_pct', 0),
                target_change=signal.get('target_change_pct', 0)
            )

    def get_active_positions(self) -> List[str]:
        """
        Get a list of currently active trading symbols.

        Returns:
            List[str]: List of active symbols.
        """
        return list(active_positions.keys())

    def get_price_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current price data for a symbol.
        Placeholder: Replace with actual price fetching logic.

        Args:
            symbol (str): The trading symbol.

        Returns:
            dict: Dictionary with at least 'current' price.
        """
        # TODO: Integrate with price feed
        return {"current": active_positions[symbol].get("last_price", 100.0)}

    def calculate_pnl(self, symbol: str) -> float:
        """
        Calculate current PnL for a symbol.
        Placeholder: Replace with actual PnL calculation.

        Args:
            symbol (str): The trading symbol.

        Returns:
            float: PnL as a decimal (e.g., 0.03 for 3%).
        """
        # TODO: Integrate with actual PnL calculation
        pos = active_positions[symbol]
        entry = pos.get("entry_price", 100.0)
        last = pos.get("last_price", 100.0)
        if entry == 0:
            return 0.0
        return (last - entry) / entry

    def _generate_schedule(self) -> List[str]:
        """
        Generate random check times (2-4 between 9:15-15:15).

        Returns:
            List[str]: List of scheduled check times as "HH:MM".
        """
        times = sorted([
            f"{random.randint(9, 14)}:{random.randint(15, 45):02d}"
            for _ in range(random.randint(2, 4))
        ])
        return times
