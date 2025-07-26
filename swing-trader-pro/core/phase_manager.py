# core/phase_manager.py
from config.logging_config import configure_logging, get_logger
from brokers.broker_adapter import BrokerAdapter
import logging
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


# method 2 best version
# core/phase_manager.py

logger = logging.getLogger(__name__)


class PhaseManager:
    """
    Orchestrates the daily trading workflow: screening, signal generation,
    monitoring, trade execution, and reporting.
    """

    def __init__(self, broker_settings):
        self.broker_settings = broker_settings
        self.screening = MorningScreening()
        self.signal = SignalGenerator()
        self.monitor = DynamicMonitor()
        self.reporting = ReportingEngine()
        self.active_symbols = []  # Ensure always initialized

    def execute_daily_cycle(self):
        """Orchestrate the complete trading day workflow"""
        # Morning screening at 8:00 AM
        schedule.every().day.at("08:00").do(self.safe_run, self.run_screening)

        # Signal generation at 9:15 AM
        schedule.every().day.at("09:15").do(self.safe_run, self.generate_signals)

        # Random monitoring checks
        self.schedule_random_checks()

        # End-of-day reporting
        schedule.every().day.at("18:00").do(self.safe_run, self.generate_reports)

        logger.info("PhaseManager started daily cycle.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("PhaseManager stopped by user.")

    def safe_run(self, func, *args, **kwargs):
        """Wrapper to safely run scheduled jobs with error handling."""
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(
                f"Exception in scheduled job {func.__name__}: {e}")

    def run_screening(self):
        """Execute morning screening phase"""
        try:
            screened = self.screening.run()
            self.active_symbols = screened if screened else []
            logger.info(f"Screened symbols: {self.active_symbols}")
        except Exception as e:
            logger.exception(f"Error during screening: {e}")
            self.active_symbols = []

    def generate_signals(self):
        """Generate trading signals from screened symbols"""
        if not self.active_symbols:
            logger.warning("No active symbols to generate signals for.")
            return
        for symbol in self.active_symbols:
            try:
                signal = self.signal.generate(symbol)
                if signal:
                    self.execute_trade(signal)
            except Exception as e:
                logger.exception(f"Error generating signal for {symbol}: {e}")

    def execute_trade(self, signal):
        """Execute trade through broker API"""
        try:
            broker = self.get_broker_adapter()
            broker.place_gtt_order(
                symbol=signal['symbol'],
                entry=signal['entry'],
                sl=signal['sl'],
                target=signal['target'],
                quantity=signal['quantity']
            )
            logger.info(f"Trade executed for {signal['symbol']}")
        except Exception as e:
            logger.exception(
                f"Trade execution failed for {signal.get('symbol', 'UNKNOWN')}: {e}")

    def get_broker_adapter(self):
        """
        Instantiate and return the broker adapter.
        Assumes BrokerAdapter takes broker_settings as argument.
        """
        return BrokerAdapter(self.broker_settings)

    def schedule_random_checks(self):
        """Schedule 2-4 random monitoring checks"""
        check_times = self.generate_random_times(2, 4)
        for check_time in check_times:
            schedule.every().day.at(check_time).do(self.safe_run, self.run_monitoring)
        logger.info(f"Scheduled monitoring checks at: {check_times}")

    def generate_random_times(self, min_checks, max_checks):
        """
        Generate random monitoring times between 9:15 and 15:15 (inclusive).
        Returns a sorted list of time strings in HH:MM format.
        """
        num_checks = random.randint(min_checks, max_checks)
        times = set()
        while len(times) < num_checks:
            hour = random.randint(9, 14)
            if hour == 9:
                minute = random.randint(15, 59)
            elif hour == 15:
                minute = 15
            else:
                minute = random.randint(0, 59)
            time_str = f"{hour:02d}:{minute:02d}"
            # Only allow up to 15:15
            if hour < 15 or (hour == 15 and minute <= 15):
                times.add(time_str)
        return sorted(times)

    def run_monitoring(self):
        """Execute dynamic monitoring checks"""
        try:
            self.monitor.check_active_positions()
            logger.info("Monitoring check completed.")
        except Exception as e:
            logger.exception(f"Error during monitoring: {e}")

    def generate_reports(self):
        """Generate end-of-day reports"""
        try:
            self.reporting.generate_daily_report()
            logger.info("End-of-day report generated.")
        except Exception as e:
            logger.exception(f"Error generating report: {e}")

# method 2


# Ensure logging is configured at import (safe if called multiple times)
configure_logging()
logger = get_logger(__name__)


class PhaseManager:
    """
    Orchestrates the daily trading workflow: screening, signal generation,
    monitoring, trade execution, and reporting.
    """

    def __init__(self, broker_settings):
        """
        Args:
            broker_settings (dict): Broker credentials/settings, must include 'broker' key.
        """
        self.broker_settings = broker_settings
        self.screening = MorningScreening()
        self.signal = SignalGenerator()
        self.monitor = DynamicMonitor()
        self.reporting = ReportingEngine()
        self.active_symbols = []  # Ensure always initialized

    def execute_daily_cycle(self):
        """Orchestrate the complete trading day workflow"""
        # Morning screening at 8:00 AM
        schedule.every().day.at("08:00").do(self.safe_run, self.run_screening)

        # Signal generation at 9:15 AM
        schedule.every().day.at("09:15").do(self.safe_run, self.generate_signals)

        # Random monitoring checks
        self.schedule_random_checks()

        # End-of-day reporting
        schedule.every().day.at("18:00").do(self.safe_run, self.generate_reports)

        logger.info("PhaseManager started daily cycle.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("PhaseManager stopped by user.")

    def safe_run(self, func, *args, **kwargs):
        """Wrapper to safely run scheduled jobs with error handling."""
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(
                f"Exception in scheduled job {func.__name__}: {e}")

    def run_screening(self):
        """Execute morning screening phase"""
        try:
            screened = self.screening.run()
            self.active_symbols = screened if screened else []
            logger.info(f"Screened symbols: {self.active_symbols}")
        except Exception as e:
            logger.exception(f"Error during screening: {e}")
            self.active_symbols = []

    def generate_signals(self):
        """Generate trading signals from screened symbols"""
        if not self.active_symbols:
            logger.warning("No active symbols to generate signals for.")
            return
        for symbol in self.active_symbols:
            try:
                signal = self.signal.generate(symbol)
                if signal:
                    self.execute_trade(signal)
            except Exception as e:
                logger.exception(f"Error generating signal for {symbol}: {e}")

    def execute_trade(self, signal):
        """Execute trade through broker API"""
        try:
            broker = self.get_broker_adapter()
            broker.place_gtt_order(
                symbol=signal['symbol'],
                entry=signal['entry'],
                sl=signal['sl'],
                target=signal['target'],
                quantity=signal['quantity']
            )
            logger.info(f"Trade executed for {signal['symbol']}")
        except Exception as e:
            logger.exception(
                f"Trade execution failed for {signal.get('symbol', 'UNKNOWN')}: {e}")

    def get_broker_adapter(self):
        """
        Instantiate and return the broker adapter.
        Expects self.broker_settings to include a 'broker' key.
        """
        broker_name = self.broker_settings.get("broker_name")
        if not broker_name:
            logger.error("broker_settings must include a 'broker' key.")
            raise ValueError("broker_settings must include a 'broker' key.")
        # Pass broker name and all settings as kwargs
        broker_kwargs = {
            k: v for k, v in self.broker_settings.items() if k != "broker_name"}
        return BrokerAdapter(broker=broker_name, **broker_kwargs)

    def schedule_random_checks(self):
        """Schedule 2-4 random monitoring checks"""
        check_times = self.generate_random_times(2, 4)
        for check_time in check_times:
            schedule.every().day.at(check_time).do(self.safe_run, self.run_monitoring)
        logger.info(f"Scheduled monitoring checks at: {check_times}")

    def generate_random_times(self, min_checks, max_checks):
        """
        Generate random monitoring times between 9:15 and 15:15 (inclusive).
        Returns a sorted list of time strings in HH:MM format.
        """
        num_checks = random.randint(min_checks, max_checks)
        times = set()
        while len(times) < num_checks:
            hour = random.randint(9, 14)
            if hour == 9:
                minute = random.randint(15, 59)
            elif hour == 15:
                minute = 15
            else:
                minute = random.randint(0, 59)
            time_str = f"{hour:02d}:{minute:02d}"
            # Only allow up to 15:15
            if hour < 15 or (hour == 15 and minute <= 15):
                times.add(time_str)
        return sorted(times)

    def run_monitoring(self):
        """Execute dynamic monitoring checks"""
        try:
            self.monitor.check_active_positions()
            logger.info("Monitoring check completed.")
        except Exception as e:
            logger.exception(f"Error during monitoring: {e}")

    def generate_reports(self):
        """Generate end-of-day reports"""
        try:
            self.reporting.generate_daily_report()
            logger.info("End-of-day report generated.")
        except Exception as e:
            logger.exception(f"Error generating report: {e}")
