# brokers/zerodha/gtt_manager.py
from kiteconnect import KiteConnect


class ZerodhaAdapter:
    def __init__(self):
        self.api_key = "your_api_key"
        self.access_token = "your_access_token"
        self.kite = KiteConnect(api_key=self.api_key)
        self.kite.set_access_token(self.access_token)

    def place_gtt_order(self, symbol, entry, sl, target, quantity):
        """Place Good-Till-Triggered order"""
        gtt_template = {
            "tradingsymbol": symbol,
            "exchange": "NSE",
            "trigger_type": "two-leg",
            "first_leg": {
                "trigger": sl,
                "price": sl * 0.98,
                "transaction_type": "SELL"
            },
            "second_leg": {
                "trigger": target,
                "price": target,
                "transaction_type": "SELL"
            },
            "validity": "1-month"
        }
        return self.kite.place_gtt(gtt_template)

    def modify_gtt(self, symbol, new_sl, new_target):
        """Modify existing GTT order"""
        # Implementation would fetch existing order first
        updated_order = {
            "trigger": {
                "lower": new_sl,
                "upper": new_target
            }
        }
        return self.kite.modify_gtt(updated_order)
