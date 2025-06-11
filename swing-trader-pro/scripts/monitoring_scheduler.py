# scripts/monitoring_scheduler.py
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
