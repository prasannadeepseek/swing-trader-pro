# phases/3_dynamic_monitoring/gtt_updater.py
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
            f"{random.randint(9,14)}:{random.randint(15,45):02d}"
            for _ in range(random.randint(2, 4))
        ])
# metod 2


class DynamicGTTManager:
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
