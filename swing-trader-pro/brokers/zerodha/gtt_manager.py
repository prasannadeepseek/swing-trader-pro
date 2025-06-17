# brokers/zerodha/gtt_manager.py
from config.broker_config import ZERODHA_API_KEY, ZERODHA_ACCESS_TOKEN
from typing import Optional, Dict, Any
import logging
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


# method 3 final version

# It's best to load credentials from a config file or environment variable

logger = logging.getLogger(__name__)


class ZerodhaGTTManager:
    """
    Adapter for placing, modifying, and deleting GTT orders via Zerodha KiteConnect.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None
    ):
        """
        Initialize the Zerodha KiteConnect client.

        Args:
            api_key (str, optional): Zerodha API key.
            access_token (str, optional): Zerodha access token.
        """
        self.api_key = api_key or ZERODHA_API_KEY
        self.access_token = access_token or ZERODHA_ACCESS_TOKEN
        self.kite = KiteConnect(api_key=self.api_key)
        self.kite.set_access_token(self.access_token)

    def place_gtt_order(
        self,
        symbol: str,
        entry: float,
        sl: float,
        target: float,
        quantity: int,
        exchange: str = "NSE"
    ) -> Optional[Dict[str, Any]]:
        """
        Place a Good-Till-Triggered (GTT) order.

        Args:
            symbol (str): Trading symbol.
            entry (float): Entry/last price.
            sl (float): Stop loss trigger value.
            target (float): Target trigger value.
            quantity (int): Order quantity.
            exchange (str): Exchange name (default "NSE").

        Returns:
            dict or None: API response or None if failed.
        """
        gtt_template = {
            "tradingsymbol": symbol,
            "exchange": exchange,
            "trigger_type": "two-leg",
            "last_price": entry,
            "orders": [
                {
                    "transaction_type": "SELL",
                    "quantity": quantity,
                    "order_type": "LIMIT",
                    "price": sl * 0.98
                },
                {
                    "transaction_type": "SELL",
                    "quantity": quantity,
                    "order_type": "LIMIT",
                    "price": target
                }
            ],
            "trigger_values": [sl, target]
        }
        try:
            response = self.kite.place_gtt(
                trigger_type="two-leg",
                tradingsymbol=symbol,
                exchange=exchange,
                trigger_values=[sl, target],
                last_price=entry,
                orders=gtt_template["orders"]
            )
            logger.info(f"GTT order placed: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to place GTT order: {e}")
            return None

    def modify_gtt(
        self,
        gtt_id: int,
        new_sl: float,
        new_target: float,
        symbol: str,
        entry: float,
        quantity: int,
        exchange: str = "NSE"
    ) -> Optional[Dict[str, Any]]:
        """
        Modify an existing GTT order.

        Args:
            gtt_id (int): GTT order ID.
            new_sl (float): New stop loss trigger value.
            new_target (float): New target trigger value.
            symbol (str): Trading symbol.
            entry (float): Last traded price.
            quantity (int): Order quantity.
            exchange (str): Exchange name.

        Returns:
            dict or None: API response or None if failed.
        """
        try:
            response = self.kite.modify_gtt(
                id=gtt_id,
                trigger_type="two-leg",
                tradingsymbol=symbol,
                exchange=exchange,
                trigger_values=[new_sl, new_target],
                last_price=entry,
                orders=[
                    {
                        "transaction_type": "SELL",
                        "quantity": quantity,
                        "order_type": "LIMIT",
                        "price": new_sl * 0.98
                    },
                    {
                        "transaction_type": "SELL",
                        "quantity": quantity,
                        "order_type": "LIMIT",
                        "price": new_target
                    }
                ]
            )
            logger.info(f"GTT order modified: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to modify GTT order: {e}")
            return None

    def delete_gtt(self, gtt_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete/cancel a GTT order.

        Args:
            gtt_id (int): GTT order ID.

        Returns:
            dict or None: API response or None if failed.
        """
        try:
            response = self.kite.delete_gtt(gtt_id)
            logger.info(f"GTT order deleted: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to delete GTT order: {e}")
            return None
