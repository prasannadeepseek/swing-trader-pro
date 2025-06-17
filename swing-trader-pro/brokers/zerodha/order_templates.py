from typing import Dict, Literal, Optional


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

# method 3 final version


class ZerodhaGTTTemplates:
    """
    Utility class for generating Zerodha GTT order templates.
    """

    @staticmethod
    def swing_order(
        symbol: str,
        entry: float,
        sl: float,
        target: float,
        quantity: int,
        exchange: str = "NSE",
        validity: str = "1-month"
    ) -> Dict:
        """
        Generate a swing GTT order template for Zerodha.

        Args:
            symbol (str): Trading symbol.
            entry (float): Entry price (not used in template, for reference).
            sl (float): Stop loss trigger price.
            target (float): Target trigger price.
            quantity (int): Quantity to sell.
            exchange (str): Exchange name. Default is "NSE".
            validity (str): Validity period. Default is "1-month".

        Returns:
            dict: GTT order template.
        """
        return {
            "tradingsymbol": symbol,
            "exchange": exchange,
            "trigger_type": "two-leg",
            "first_leg": {
                "trigger": sl,
                "price": round(sl * 0.98, 2),
                "transaction_type": "SELL",
                "quantity": quantity
            },
            "second_leg": {
                "trigger": target,
                "price": round(target, 2),
                "transaction_type": "SELL",
                "quantity": quantity
            },
            "validity": validity
        }

    @staticmethod
    def two_leg_gtt(
        symbol: str,
        sl: float,
        target: float,
        quantity: int,
        transaction_type: Literal["SELL", "BUY"] = "SELL",
        exchange: str = "NSE",
        validity: str = "1-month"
    ) -> Dict:
        """
        Generate a generic two-leg GTT order template.

        Args:
            symbol (str): Trading symbol.
            sl (float): Stop loss trigger price.
            target (float): Target trigger price.
            quantity (int): Quantity to trade.
            transaction_type (str): "SELL" or "BUY". Default is "SELL".
            exchange (str): Exchange name. Default is "NSE".
            validity (str): Validity period. Default is "1-month".

        Returns:
            dict: GTT order template.
        """
        return {
            "tradingsymbol": symbol,
            "exchange": exchange,
            "trigger_type": "two-leg",
            "first_leg": {
                "trigger": sl,
                "price": round(sl * 0.98, 2) if transaction_type == "SELL" else round(sl * 1.02, 2),
                "transaction_type": transaction_type,
                "quantity": quantity
            },
            "second_leg": {
                "trigger": target,
                "price": round(target, 2),
                "transaction_type": transaction_type,
                "quantity": quantity
            },
            "validity": validity
        }
