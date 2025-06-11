# swing-trader-pro/main.py
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
