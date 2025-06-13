# phases/1_morning_screening/institutional_flow.py
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
