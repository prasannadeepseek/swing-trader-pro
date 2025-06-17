# brokers/upstox/gtt_manager.py
from config.broker_config import UPSTOX_API_KEY, UPSTOX_ACCESS_TOKEN
import logging
from typing import Optional, List, Any, Dict
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

# method 3 final version

# Optionally, load these from a config file or environment variables


logger = logging.getLogger(__name__)


class UpstoxGTTManager:
    """
    Manager for placing, modifying, and deleting GTT orders on Upstox.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None
    ):
        """
        Initialize the Upstox client.

        Args:
            api_key (str, optional): Upstox API key.
            access_token (str, optional): Upstox access token.
        """
        self.client = Upstox(
            api_key or UPSTOX_API_KEY,
            access_token or UPSTOX_ACCESS_TOKEN
        )

    def place_gtt_order(
        self,
        symbol: str,
        entry: float,
        sl: float,
        target: float,
        quantity: int,
        exchange: str = 'NSE',
        order_type: str = 'LIMIT',
        product: str = 'MIS',
        duration: str = 'DAY',
        trigger_type: str = 'two-leg'
    ) -> Optional[Dict[str, Any]]:
        """
        Place a GTT order on Upstox.

        Args:
            symbol (str): Trading symbol.
            entry (float): Entry/last price.
            sl (float): Stop loss trigger value.
            target (float): Target trigger value.
            quantity (int): Order quantity.
            exchange (str): Exchange (default 'NSE').
            order_type (str): Order type (default 'LIMIT').
            product (str): Product type (default 'MIS').
            duration (str): Order duration (default 'DAY').
            trigger_type (str): GTT trigger type (default 'two-leg').

        Returns:
            dict or None: API response or None if failed.
        """
        try:
            response = self.client.place_gtt(
                trigger_type=trigger_type,
                tradingsymbol=symbol,
                exchange=exchange,
                trigger_values=[sl, target],
                last_price=entry,
                quantity=quantity,
                disclosed_quantity=0,
                order_type=order_type,
                product=product,
                duration=duration
            )
            logger.info(f"GTT order placed: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to place GTT order: {e}")
            return None

    def modify_gtt(
        self,
        gtt_id: str,
        new_sl: float,
        new_target: float
    ) -> Optional[Dict[str, Any]]:
        """
        Modify an existing GTT order.

        Args:
            gtt_id (str): GTT order ID.
            new_sl (float): New stop loss trigger value.
            new_target (float): New target trigger value.

        Returns:
            dict or None: API response or None if failed.
        """
        try:
            response = self.client.modify_gtt(
                id=gtt_id,
                trigger_values=[new_sl, new_target]
            )
            logger.info(f"GTT order modified: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to modify GTT order: {e}")
            return None

    def delete_gtt(self, gtt_id: str) -> Optional[Dict[str, Any]]:
        """
        Delete/cancel a GTT order.

        Args:
            gtt_id (str): GTT order ID.

        Returns:
            dict or None: API response or None if failed.
        """
        try:
            response = self.client.cancel_gtt(id=gtt_id)
            logger.info(f"GTT order deleted: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to delete GTT order: {e}")
            return None
