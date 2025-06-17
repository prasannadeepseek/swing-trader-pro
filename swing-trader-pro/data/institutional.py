# data/institutional.py
from typing import Optional, Dict


class InstitutionalData:
    @staticmethod
    def recent_selling(symbol):
        # Implement institutional data check
        return False
# method 2 final version
# data/institutional.py


class InstitutionalData:
    """
    Provides methods to check recent institutional activity (buying/selling)
    for a given symbol. In a real implementation, this would fetch and cache
    data from an external source (e.g., NSE/BSE bulk/block deals, FII/DII data).
    """

    _institutional_activity: Dict[str, Dict[str, float]] = {}

    @classmethod
    def update_data(cls, symbol: str, net_buy: float, net_sell: float) -> None:
        """
        Update the institutional activity data for a symbol.

        Args:
            symbol (str): The trading symbol.
            net_buy (float): Net buy volume/value.
            net_sell (float): Net sell volume/value.
        """
        cls._institutional_activity[symbol] = {
            "net_buy": net_buy,
            "net_sell": net_sell
        }

    @classmethod
    def recent_selling(cls, symbol: str, threshold: float = 1_00_000) -> bool:
        """
        Check if there has been recent significant institutional selling.

        Args:
            symbol (str): The trading symbol.
            threshold (float): Minimum sell value to consider as 'significant'.

        Returns:
            bool: True if recent selling exceeds threshold, else False.
        """
        data = cls._institutional_activity.get(symbol)
        return data is not None and data.get("net_sell", 0) > threshold

    @classmethod
    def recent_buying(cls, symbol: str, threshold: float = 1_00_000) -> bool:
        """
        Check if there has been recent significant institutional buying.

        Args:
            symbol (str): The trading symbol.
            threshold (float): Minimum buy value to consider as 'significant'.

        Returns:
            bool: True if recent buying exceeds threshold, else False.
        """
        data = cls._institutional_activity.get(symbol)
        return data is not None and data.get("net_buy", 0) > threshold

    @classmethod
    def net_activity(cls, symbol: str) -> Optional[float]:
        """
        Get the net institutional activity (buy - sell) for a symbol.

        Args:
            symbol (str): The trading symbol.

        Returns:
            float or None: Net activity value, or None if no data.
        """
        data = cls._institutional_activity.get(symbol)
        if data is None:
            return None
        return data.get("net_buy", 0) - data.get("net_sell", 0)
