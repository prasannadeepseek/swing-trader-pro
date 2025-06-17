# phases/1_morning_screening/institutional_flow.py
from typing import Dict, Any, Optional, List
import requests
# from config.constraints import CAP_THRESHOLDS
from config import constraints


class InstitutionalScreener:
    def __init__(self):
        self.api_endpoint = "https://fii-dii-data.com/latest"

    def screen(self):
        """Screen stocks based on institutional flows"""
        data = self.fetch_institutional_data()
        screened = {}

        for symbol, metrics in data.items():
            cap_type = self.get_cap_type(symbol)
            threshold = constraints.CAP_THRESHOLDS[cap_type]

            if metrics['net_3day'] >= threshold:
                screened[symbol] = {
                    'fii_net': metrics['fii_net'],
                    'dii_net': metrics['dii_net'],
                    'delivery_pct': metrics['delivery_pct'],
                    'cap_type': cap_type
                }
        return screened

    def fetch_institutional_data(self):
        """Fetch FII/DII data from API"""
        response = requests.get(self.api_endpoint)
        return response.json()

    def get_cap_type(self, symbol):
        """Classify stock by market cap"""
        # Implementation would use market cap data
        if symbol in ['RELIANCE', 'HDFCBANK']:
            return 'large'
        elif symbol in ['PEL', 'DEEPAKNTR']:
            return 'mid'
        return 'small'
# method 2


class InstitutionalScreener:
    CAP_THRESHOLDS = {
        'large': 4e7,  # 4Cr
        'mid': 3e7,
        'small': 1e7
    }

    def screen(self, institutional_data):
        screened = {}
        for symbol, metrics in institutional_data.items():
            cap_type = self._get_cap_type(symbol)
            if metrics['net_3day'] >= self.CAP_THRESHOLDS[cap_type]:
                screened[symbol] = {
                    'fii_net': metrics['fii_net'],
                    'dii_net': metrics['dii_net'],
                    'delivery_pct': metrics['delivery_pct']
                }
        return screened
# method 3
# phases/1_morning_screening/institutional_flow.py


class InstitutionalScreener:
    def __init__(self):
        self.data_pipeline = DataPipeline()

    def get_enhanced_flows(self, symbol):
        """Fetch complete institutional data"""
        flows = self.data_pipeline.fetch_fii_activity()
        oi_data = self.data_pipeline.fetch_oi_changes()
        block_deals = self.data_pipeline.fetch_block_deals()

        return {
            'symbol': symbol,
            'fii_flows': self._process_flows(flows),
            'oi_changes': self._process_oi(oi_data),
            'block_deals': self._match_block_deals(symbol, block_deals)
        }

    def _match_block_deals(self, symbol, deals):
        """Verify if FII buying matches block deals"""
        return [d for d in deals if d['symbol'] == symbol]

# method 4 final version


try:
    from config import constraints
    CAP_THRESHOLDS = constraints.CAP_THRESHOLDS
except ImportError:
    # Fallback if constraints module is not available
    CAP_THRESHOLDS = {
        'large': 4e7,  # 4Cr
        'mid': 3e7,
        'small': 1e7
    }


class DataPipeline:
    """
    Placeholder for the actual DataPipeline implementation.
    Replace with the real import in production.
    """

    def fetch_fii_activity(self):
        return {}

    def fetch_oi_changes(self):
        return {}

    def fetch_block_deals(self):
        return []


class InstitutionalScreener:
    """
    Screens stocks based on institutional flows, supporting both API and data pipeline sources.
    Provides enhanced institutional flow analysis including FII/DII activity, OI changes, and block deals.
    """

    def __init__(
        self,
        use_api: bool = True,
        api_endpoint: str = "https://fii-dii-data.com/latest",
        cap_thresholds: Optional[Dict[str, float]] = None,
        data_pipeline: Optional[Any] = None
    ):
        """
        Args:
            use_api (bool): If True, fetch data from API; else use data pipeline.
            api_endpoint (str): API endpoint for institutional data.
            cap_thresholds (dict): Optional override for cap thresholds.
            data_pipeline: Optional data pipeline object for advanced data fetching.
        """
        self.use_api = use_api
        self.api_endpoint = api_endpoint
        self.cap_thresholds = cap_thresholds or CAP_THRESHOLDS
        self.data_pipeline = data_pipeline or DataPipeline()

    def screen(self, institutional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Screen stocks based on institutional flows and cap thresholds.

        Args:
            institutional_data (dict, optional): If provided, use this data instead of fetching.

        Returns:
            dict: Screened symbols with relevant metrics.
        """
        if institutional_data is None:
            if self.use_api:
                data = self.fetch_institutional_data()
            else:
                data = self.data_pipeline.fetch_fii_activity()
        else:
            data = institutional_data

        screened = {}
        for symbol, metrics in data.items():
            cap_type = self.get_cap_type(symbol)
            threshold = self.cap_thresholds.get(cap_type, 1e7)
            if metrics.get('net_3day', 0) >= threshold:
                screened[symbol] = {
                    'fii_net': metrics.get('fii_net'),
                    'dii_net': metrics.get('dii_net'),
                    'delivery_pct': metrics.get('delivery_pct'),
                    'cap_type': cap_type
                }
        return screened

    def fetch_institutional_data(self) -> Dict[str, Any]:
        """
        Fetch FII/DII data from the configured API endpoint.

        Returns:
            dict: Institutional data keyed by symbol.
        """
        try:
            response = requests.get(self.api_endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching institutional data: {e}")
            return {}

    def get_cap_type(self, symbol: str) -> str:
        """
        Classify stock by market cap.

        Args:
            symbol (str): Trading symbol.

        Returns:
            str: 'large', 'mid', or 'small'
        """
        # Example logic; replace with actual market cap lookup
        if symbol in ['RELIANCE', 'HDFCBANK']:
            return 'large'
        elif symbol in ['PEL', 'DEEPAKNTR']:
            return 'mid'
        return 'small'

    def get_enhanced_flows(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch and aggregate complete institutional data for a symbol.

        Args:
            symbol (str): Trading symbol.

        Returns:
            dict: Aggregated institutional flow data.
        """
        flows = self.data_pipeline.fetch_fii_activity()
        oi_data = self.data_pipeline.fetch_oi_changes()
        block_deals = self.data_pipeline.fetch_block_deals()

        return {
            'symbol': symbol,
            'fii_flows': self._process_flows(flows, symbol),
            'oi_changes': self._process_oi(oi_data, symbol),
            'block_deals': self._match_block_deals(symbol, block_deals)
        }

    def _process_flows(self, flows: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """Extract FII flows for the symbol."""
        return flows.get(symbol, {})

    def _process_oi(self, oi_data: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """Extract OI changes for the symbol."""
        return oi_data.get(symbol, {})

    def _match_block_deals(self, symbol: str, deals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return block deals matching the symbol."""
        return [d for d in deals if d.get('symbol') == symbol]
