# core/phase_manager.py
import schedule
import time
from datetime import datetime, timedelta
import random
from phases import (
    MorningScreening,
    SignalGenerator,
    DynamicMonitor,
    ReportingEngine
)


class PhaseManager:
    def __init__(self, broker_settings):
        self.broker_settings = broker_settings
        self.screening = MorningScreening()
        self.signal = SignalGenerator()
        self.monitor = DynamicMonitor()
        self.reporting = ReportingEngine()

    def execute_daily_cycle(self):
        """Orchestrate the complete trading day workflow"""
        # Morning screening at 8:00 AM
        schedule.every().day.at("08:00").do(self.run_screening)

        # Signal generation at 9:15 AM
        schedule.every().day.at("09:15").do(self.generate_signals)

        # Random monitoring checks
        self.schedule_random_checks()

        # End-of-day reporting
        schedule.every().day.at("18:00").do(self.generate_reports)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_screening(self):
        """Execute morning screening phase"""
        screened = self.screening.run()
        self.active_symbols = screened  # Store for signal generation

    def generate_signals(self):
        """Generate trading signals from screened symbols"""
        for symbol in self.active_symbols:
            signal = self.signal.generate(symbol)
            if signal:
                self.execute_trade(signal)

    def execute_trade(self, signal):
        """Execute trade through broker API"""
        broker = self.get_broker_adapter()
        broker.place_gtt_order(
            symbol=signal['symbol'],
            entry=signal['entry'],
            sl=signal['sl'],
            target=signal['target'],
            quantity=signal['quantity']
        )

    def schedule_random_checks(self):
        """Schedule 2-4 random monitoring checks"""
        check_times = self.generate_random_times(2, 4)
        for check_time in check_times:
            schedule.every().day.at(check_time).do(self.run_monitoring)

    def generate_random_times(self, min_checks, max_checks):
        """Generate random monitoring times between 9:15-15:15"""
        num_checks = random.randint(min_checks, max_checks)
        return sorted([
            f"{random.randint(9,14)}:{random.randint(15,45):02d}"
            for _ in range(num_checks)
        ])

    def run_monitoring(self):
        """Execute dynamic monitoring checks"""
        self.monitor.check_active_positions()

    def generate_reports(self):
        """Generate end-of-day reports"""
        self.reporting.generate_daily_report()
