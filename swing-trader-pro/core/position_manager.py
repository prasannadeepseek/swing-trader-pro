# core/position_manager.py
from typing import Dict, Any
active_positions = {}  # This would be more complex in reality


def update_positions(symbol, data):
    active_positions[symbol] = data
# method 3 final version
# core/position_manager.py


active_positions: Dict[str, Dict[str, Any]] = {}


def enter_position(symbol: str, data: Dict[str, Any]) -> None:
    """
    Enter a new position for the given symbol.
    Args:
        symbol (str): The trading symbol.
        data (dict): Position details (e.g., entry_price, quantity, timestamp, etc.)
    """
    active_positions[symbol] = data
    print(f"Entered position for {symbol}: {data}")


def exit_position(symbol: str) -> None:
    """
    Exit the position for the given symbol.
    Args:
        symbol (str): The trading symbol.
    """
    if symbol in active_positions:
        exited = active_positions.pop(symbol)
        print(f"Exited position for {symbol}: {exited}")
    else:
        print(f"No active position to exit for {symbol}.")


def update_position(symbol: str, data: Dict[str, Any]) -> None:
    """
    Update the position for the given symbol.
    Args:
        symbol (str): The trading symbol.
        data (dict): Updated position details.
    """
    if symbol in active_positions:
        active_positions[symbol].update(data)
        print(f"Updated position for {symbol}: {active_positions[symbol]}")
    else:
        print(f"No active position to update for {symbol}.")


def is_active(symbol: str) -> bool:
    """
    Check if a position is active for the given symbol.
    Args:
        symbol (str): The trading symbol.
    Returns:
        bool: True if active, False otherwise.
    """
    return symbol in active_positions


def get_position(symbol: str) -> Dict[str, Any]:
    """
    Get the current position data for a symbol.
    Args:
        symbol (str): The trading symbol.
    Returns:
        dict: Position data or empty dict if not active.
    """
    return active_positions.get(symbol, {})
