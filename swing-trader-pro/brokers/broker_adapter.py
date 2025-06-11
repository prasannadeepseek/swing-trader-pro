# brokers/broker_adapter.py
from brokers.zerodha.gtt_manager import ZerodhaGTTManager
from brokers.upstox.gtt_manager import UpstoxGTTManager


class BrokerAdapter:
    def __init__(self):
        self.broker = ZerodhaGTTManager()  # Default to Zerodha

    def modify_gtt(self, symbol, new_sl, new_target):
        return self.broker.modify_gtt(symbol, new_sl, new_target)
