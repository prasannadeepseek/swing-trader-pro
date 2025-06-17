from typing import Any, Dict, Optional, List
from kiteconnect import KiteConnect
import pandas as pd


class BrokerDataFetcher:

    def __init__(self, api_key, access_token):
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)

    def get_fii_derivatives_positions(self):
        """Fetch FII positions in derivatives"""
        positions = self.kite.positions()
        return pd.DataFrame([
            {
                'symbol': p['tradingsymbol'],
                'net_qty': p['net_quantity'],
                'oi': p['open_quantity']
            }
            for p in positions['net']
            if p['product'] == 'FUT'
        ])

    def get_block_deals(self):
        """Fetch broker-specific block deal info"""
        # Implementation varies by broker
        return self.kite.get_block_deals()

# method 3 final version


try:
    from kiteconnect import KiteConnect
except ImportError:
    KiteConnect = None  # For environments where kiteconnect isn't installed


class BrokerDataFetcher:
    """
    Unified data fetcher for broker APIs (currently supports Zerodha Kite).
    Designed for extensibility to other brokers.
    """

    def __init__(self, api_key: str, access_token: str, broker: str = "zerodha"):
        """
        Initialize the broker client.

        Args:
            api_key (str): API key for the broker.
            access_token (str): Access token for the broker.
            broker (str): Broker name (default: "zerodha").
        """
        self.broker = broker.lower()
        if self.broker == "zerodha":
            if KiteConnect is None:
                raise ImportError(
                    "kiteconnect package is required for Zerodha integration.")
            self.client = KiteConnect(api_key=api_key)
            self.client.set_access_token(access_token)
        else:
            raise NotImplementedError(
                f"Broker '{broker}' is not supported yet.")

    def get_fii_derivatives_positions(self) -> pd.DataFrame:
        """
        Fetch FII positions in derivatives (currently supports Zerodha only).

        Returns:
            pd.DataFrame: DataFrame with columns ['symbol', 'net_qty', 'oi'].
        """
        try:
            positions = self.client.positions()
            data = [
                {
                    'symbol': p['tradingsymbol'],
                    'net_qty': p['net_quantity'],
                    'oi': p.get('open_quantity', 0)
                }
                for p in positions.get('net', [])
                if p.get('product') == 'FUT'
            ]
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error fetching FII derivatives positions: {e}")
            return pd.DataFrame(columns=['symbol', 'net_qty', 'oi'])

    def get_block_deals(self) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch block deal information (broker-specific).

        Returns:
            List[Dict[str, Any]] or None: List of block deals or None if not implemented.
        """
        if self.broker == "zerodha":
            try:
                # Not all KiteConnect installations have get_block_deals
                if hasattr(self.client, "get_block_deals"):
                    return self.client.get_block_deals()
                else:
                    print(
                        "get_block_deals not implemented in this KiteConnect version.")
                    return None
            except Exception as e:
                print(f"Error fetching block deals: {e}")
                return None
        else:
            print(f"Block deals not supported for broker '{self.broker}'.")
            return None
