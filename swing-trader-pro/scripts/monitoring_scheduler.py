# scripts/monitoring_scheduler.py
import sys
import signal
import logging
import schedule
import time
from phases.dynamic_monitoring import DynamicMonitor


def run_monitoring_checks():
    monitor = DynamicMonitor()
    monitor.run_checks()


if __name__ == "__main__":
    # Schedule checks every 30 minutes during market hours
    schedule.every(30).minutes.between(
        "09:15", "15:15").do(run_monitoring_checks)

    while True:
        schedule.run_pending()
        time.sleep(60)
# method 2 final version
# scripts/monitoring_scheduler.py

logger = logging.getLogger("monitoring_scheduler")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def run_monitoring_checks(monitor=None):
    """
    Run monitoring checks using the provided DynamicMonitor instance.
    """
    try:
        if monitor is None:
            monitor = DynamicMonitor()
        monitor.run_checks()
        logger.info("Monitoring checks completed successfully.")
    except Exception as e:
        logger.exception(f"Error during monitoring checks: {e}")


def graceful_exit(signum, frame):
    logger.info("Received termination signal. Exiting gracefully.")
    sys.exit(0)


def main():
    """
    Main loop for scheduling monitoring checks every 30 minutes during market hours.
    """
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)

    monitor = DynamicMonitor()
    # Schedule checks every 30 minutes during market hours
    schedule.every(30).minutes.between("09:15", "15:15").do(
        run_monitoring_checks, monitor=monitor)

    logger.info("Monitoring scheduler started. Waiting for scheduled tasks...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except Exception as e:
        logger.exception(f"Scheduler encountered an error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
