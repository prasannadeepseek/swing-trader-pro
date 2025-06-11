# brokers/upstox/order_templates.py
class UpstoxOrderTemplates:
    @staticmethod
    def swing_order(symbol, entry, sl, target, quantity):
        return {
            "exchange": "NSE",
            "tradingsymbol": symbol,
            "transaction_type": "BUY",
            "order_type": "SL-M",
            "quantity": quantity,
            "price": entry,
            "trigger_price": entry,
            "squareoff": target,
            "stoploss": sl,
            "trailing_stoploss": 0.5,  # 0.5% trailing
            "product": "CNC",
            "validity": "DAY"
        }
