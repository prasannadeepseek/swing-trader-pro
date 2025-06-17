# brokers/upstox/order_templates.py
from typing import Dict, Literal, Optional


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
# method 2 final version
# swing-trader-pro/brokers/upstox/order_templates.py


class UpstoxOrderTemplates:
    """
    Utility class for generating Upstox order templates for swing and GTT orders.
    """

    @staticmethod
    def swing_order(
        symbol: str,
        entry: float,
        sl: float,
        target: float,
        quantity: int,
        transaction_type: Literal["BUY", "SELL"] = "BUY",
        product: Literal["CNC", "MIS"] = "CNC",
        trailing_stoploss: Optional[float] = 0.5
    ) -> Dict:
        """
        Generate a swing order template.

        Args:
            symbol (str): Trading symbol.
            entry (float): Entry price.
            sl (float): Stop loss price.
            target (float): Target price.
            quantity (int): Quantity to trade.
            transaction_type (str): "BUY" or "SELL". Default is "BUY".
            product (str): "CNC" (delivery) or "MIS" (intraday). Default is "CNC".
            trailing_stoploss (float, optional): Trailing stoploss percent. Default is 0.5.

        Returns:
            dict: Order template dictionary.
        """
        return {
            "exchange": "NSE",
            "tradingsymbol": symbol,
            "transaction_type": transaction_type,
            "order_type": "SL-M",
            "quantity": quantity,
            "price": entry,
            "trigger_price": entry,
            "squareoff": target,
            "stoploss": sl,
            "trailing_stoploss": trailing_stoploss,
            "product": product,
            "validity": "DAY"
        }

    @staticmethod
    def gtt_order(
        symbol: str,
        entry: float,
        sl: float,
        target: float,
        quantity: int,
        transaction_type: Literal["BUY", "SELL"] = "BUY",
        exchange: str = "NSE"
    ) -> Dict:
        """
        Generate a GTT order template.

        Args:
            symbol (str): Trading symbol.
            entry (float): Entry/last price.
            sl (float): Stop loss trigger value.
            target (float): Target trigger value.
            quantity (int): Quantity to trade.
            transaction_type (str): "BUY" or "SELL". Default is "BUY".
            exchange (str): Exchange name. Default is "NSE".

        Returns:
            dict: GTT order template dictionary.
        """
        return {
            "exchange": exchange,
            "tradingsymbol": symbol,
            "transaction_type": transaction_type,
            "trigger_values": [sl, target],
            "last_price": entry,
            "quantity": quantity,
            "order_type": "LIMIT",
            "product": "CNC",
            "validity": "DAY"
        }
