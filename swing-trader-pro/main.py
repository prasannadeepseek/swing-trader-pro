# swing-trader-pro/main.py
import sys
import signal
import argparse
from core.phase_manager import PhaseManager
from config.broker_config import BROKER_SETTINGS
from config.logging_config import configure_logging, get_logger


def graceful_exit(signum, frame):
    logger = get_logger(__name__)
    logger.info("Received termination signal. Shutting down gracefully...")
    sys.exit(0)


def main():
    # Configure logging once at the entry point
    configure_logging()
    logger = get_logger(__name__)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)

    parser = argparse.ArgumentParser(
        description="Swing Trader Pro - Automated Trading System")
    parser.add_argument(
        "--broker",
        type=str,
        default="zerodha",
        help="Broker to use (default: zerodha)"
    )
    args = parser.parse_args()

    broker_settings = BROKER_SETTINGS.get(args.broker.lower())
    if not broker_settings:
        logger.error(f"Broker '{args.broker}' not found in configuration.")
        sys.exit(1)
    # Initialize system
    phase_manager = PhaseManager(broker_settings)
    # Run complete daily cycle
    try:
        logger.info("Starting Swing Trader Pro daily cycle...")
        phase_manager.execute_daily_cycle()
    except Exception as e:
        logger.exception(f"System failure: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
