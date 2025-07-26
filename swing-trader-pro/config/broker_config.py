# config/broker_config.py
import json
import os
from typing import Dict, Any, Optional

# Path to the JSON config file (adjust if needed)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data_sources.json")


def _load_broker_settings() -> Dict[str, Dict[str, Any]]:
    """
    Load broker settings from the data_sources.json file.
    Returns:
        dict: Dictionary of broker settings.
    """
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        brokers = config.get("brokers", {})
        return brokers
    except Exception as e:
        print(f"[broker_config] Error loading broker settings: {e}")
        return {}


# Load once at module import
BROKER_SETTINGS: Dict[str, Dict[str, Any]] = _load_broker_settings()


def get_broker_credentials(broker: str) -> Optional[Dict[str, Any]]:
    """
    Safely fetch credentials/settings for a given broker.

    Args:
        broker (str): The broker name (e.g., 'zerodha', 'upstox').

    Returns:
        dict or None: The broker's settings dictionary, or None if not found.
    """
    creds = BROKER_SETTINGS.get(broker.lower())
    if creds is None:
        print(
            f"[broker_config] Warning: No credentials found for broker '{broker}'.")
    return creds
