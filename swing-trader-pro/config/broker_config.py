# config/broker_config.py
from typing import Dict, Any, Optional
BROKER_SETTINGS = {
    "zerodha": {
        "api_key": "your_api_key",
        "access_token": "your_access_token"
    },
    "telegram": {
        "token": "your_bot_token",
        "chat_id": "your_chat_id"
    }
}
# method 3 final version
# config/broker_config.py


BROKER_SETTINGS: Dict[str, Dict[str, Any]] = {
    "zerodha": {
        "api_key": "your_api_key",
        "access_token": "your_access_token"
    },
    "telegram": {
        "token": "your_bot_token",
        "chat_id": "your_chat_id"
    }
}


def get_broker_credentials(broker: str) -> Optional[Dict[str, Any]]:
    """
    Safely fetch credentials/settings for a given broker.

    Args:
        broker (str): The broker name (e.g., 'zerodha', 'telegram').

    Returns:
        dict or None: The broker's settings dictionary, or None if not found.
    """
    creds = BROKER_SETTINGS.get(broker.lower())
    if creds is None:
        print(
            f"[broker_config] Warning: No credentials found for broker '{broker}'.")
    return creds
