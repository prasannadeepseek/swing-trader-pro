# core/position_manager.py
active_positions = {}  # This would be more complex in reality


def update_positions(symbol, data):
    active_positions[symbol] = data
