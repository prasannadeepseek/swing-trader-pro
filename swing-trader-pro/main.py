# swing-trader-pro/main.py
import sys
import signal
import argparse
from core.phase_manager import PhaseManager
from config.broker_config import BROKER_SETTINGS
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize system
    phase_manager = PhaseManager(BROKER_SETTINGS)

    try:
        # Run complete daily cycle
        phase_manager.execute_daily_cycle()
    except Exception as e:
        logger.error(f"System failure: {str(e)}")
        raise


if __name__ == "__main__":
    main()

# method 2 final version
# swing-trader-pro/main.py


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    return logging.getLogger(__name__)


def graceful_exit(signum, frame):
    logger = logging.getLogger(__name__)
    logger.info("Received termination signal. Shutting down gracefully...")
    sys.exit(0)


def main():
    logger = setup_logging()

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

    phase_manager = PhaseManager(broker_settings)

    try:
        logger.info("Starting Swing Trader Pro daily cycle...")
        phase_manager.execute_daily_cycle()
    except Exception as e:
        logger.exception(f"System failure: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
