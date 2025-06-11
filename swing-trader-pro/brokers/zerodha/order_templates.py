class ZerodhaGTTTemplates:
    @staticmethod
    def swing_order(symbol, entry, sl, target, quantity):
        return {
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
            "validity": "1-month"  # Max allowed duration
        }
