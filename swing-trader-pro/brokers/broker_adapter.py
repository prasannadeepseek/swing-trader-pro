# brokers/broker_adapter.py
from brokers.zerodha.gtt_manager import ZerodhaGTTManager
from brokers.upstox.gtt_manager import UpstoxGTTManager


# method 3 final version


class BrokerAdapter:
    """
    Adapter to unify GTT management across supported brokers (Zerodha, Upstox).
    """

    def __init__(self, broker: str = "zerodha", **broker_kwargs):
        """
        Initialize the broker adapter.

        Args:
            broker (str): Broker name, "zerodha" or "upstox".
            broker_kwargs: Additional keyword arguments for broker manager initialization.
        """
        if broker.lower() == "zerodha":
            self.broker = ZerodhaGTTManager(**broker_kwargs)
            self.broker_name = "zerodha"
        elif broker.lower() == "upstox":
            self.broker = UpstoxGTTManager(**broker_kwargs)
            self.broker_name = "upstox"
        else:
            raise ValueError(f"Unsupported broker: {broker}")

    def modify_gtt(self, *args, **kwargs):
        """
        Modify a GTT order. Arguments depend on the broker:
        - Zerodha: (gtt_id, new_sl, new_target, symbol, entry, quantity, exchange)
        - Upstox: (gtt_id, new_sl, new_target)
        """
        return self.broker.modify_gtt(*args, **kwargs)

    def place_gtt_order(self, *args, **kwargs):
        """
        Place a GTT order. Arguments depend on the broker.
        """
        return self.broker.place_gtt_order(*args, **kwargs)

    def delete_gtt(self, *args, **kwargs):
        """
        Delete/cancel a GTT order. Arguments depend on the broker.
        """
        return self.broker.delete_gtt(*args, **kwargs)
