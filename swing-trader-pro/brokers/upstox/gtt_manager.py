# brokers/upstox/gtt_manager.py
from upstox_api.api import Upstox


class UpstoxGTTManager:
    def __init__(self):
        self.client = Upstox(
            api_key="your_api_key",
            access_token="your_access_token"
        )

    def place_gtt_order(self, symbol, entry, sl, target, quantity):
        """Place GTT order on Upstox"""
        return self.client.place_gtt(
            trigger_type='two-leg',
            tradingsymbol=symbol,
            exchange='NSE',
            trigger_values=[sl, target],
            last_price=entry,
            quantity=quantity,
            disclosed_quantity=0,
            order_type='LIMIT',
            product='MIS',
            duration='DAY'
        )

    def modify_gtt(self, gtt_id, new_sl, new_target):
        """Modify existing GTT order"""
        return self.client.modify_gtt(
            id=gtt_id,
            trigger_values=[new_sl, new_target]
        )
