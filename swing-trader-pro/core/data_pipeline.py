# core/data_pipeline.py
from datetime import datetime
import logging
from data_providers import NSEFetcher, NSDLFetcher, BlockDealFetcher
from brokers.data_integration import BrokerDataFetcher
from data_providers import (
    NSEFetcher,
    NSDLFetcher,
    BlockDealFetcher
)
import requests
import pandas as pd
from datetime import datetime, timedelta


class DataPipeline:
    def __init__(self):
        self.sources = {
            'price': 'https://marketdata.api/price',
            'volume': 'https://marketdata.api/volume',
            'fii_cash': 'https://nsdl.com/fii_cash',
            'fii_derivatives': 'https://nsdl.com/fii_fno',
            'block_deals': 'https://nseindia.com/block_deals',
            'oi_data': 'https://nseindia.com/oi'
        }

    def fetch_data(self, symbol, days=30):
        """Fetch and normalize data from multiple sources"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        price_data = self._fetch_from_api(
            self.sources['price'],
            symbol,
            start_date,
            end_date
        )

        volume_data = self._fetch_from_api(
            self.sources['volume'],
            symbol,
            start_date,
            end_date
        )

        return pd.merge(price_data, volume_data, on='date')

    def _fetch_from_api(self, endpoint, symbol, start, end):
        """Generic API fetcher with retry logic"""
        # Implementation would use requests with retry
        return pd.DataFrame()  # Mock response

    def fetch_fii_activity(self, days=3):
        """Fetch FII activity across segments"""
        cash = self._fetch_data('fii_cash', days)
        derivatives = self._fetch_data('fii_derivatives', days)
        return pd.merge(cash, derivatives, on='date', suffixes=('_cash', '_fno'))

    def fetch_block_deals(self):
        """Get recent block deals"""
        return requests.get(self.sources['block_deals']).json()

    def fetch_oi_changes(self):
        """Fetch Open Interest changes"""
        return requests.get(self.sources['oi_data']).json()


# method 3


class DataPipeline:

    def __init__(self, broker_api=None):
        self.broker = BrokerDataFetcher(**broker_api) if broker_api else None

    def get_institutional_data(self, symbol):
        """Combine all institutional data sources"""
        return {
            'ohlc': NSEFetcher.get_ohlc(symbol),
            'fii_flows': NSDLFetcher.get_fii_dii_activity(),
            'block_deals': BlockDealFetcher.get_recent_block_deals(),
            'derivatives_oi': self._get_derivatives_data(symbol),
            'sector_flows': NSDLFetcher.get_sector_flows()
        }

    def _get_derivatives_data(self, symbol):
        if self.broker:
            return self.broker.get_fii_derivatives_positions()
        return NSEFetcher.get_fno_oi(symbol)

# method 4


logger = logging.getLogger(__name__)


class DataPipeline:

    def __init__(self):
        self.nse = NSEFetcher()
        self.nsdl = NSDLFetcher()
        self.block = BlockDealFetcher()
        self._last_fetch_time = {}

    def get_institutional_data(self, symbol):
        """Main method with all safety features"""
        try:
            data = {
                'timestamp': datetime.now(),
                'ohlc': self._get_with_fallback(
                    self.nse.get_ohlc, symbol),
                'fii_flows': self._get_with_fallback(
                    self.nsdl.get_fii_dii_activity),
                'block_deals': self._get_with_fallback(
                    self.block.get_recent_block_deals),
                'derivatives_oi': self._get_with_fallback(
                    self.nse.get_index_oi)
            }
            self._validate_completeness(data)
            return data
        except Exception as e:
            logger.critical(f"Data pipeline failed: {str(e)}")
            return self._load_full_fallback(symbol)

    def _get_with_fallback(self, fetcher_method, *args):
        """Wrapper with logging and timing"""
        start = datetime.now()
        try:
            data = fetcher_method(*args)
            elapsed = (datetime.now() - start).total_seconds()
            logger.info(f"Fetched {fetcher_method.__name__} in {elapsed:.2f}s")
            return data
        except Exception as e:
            logger.warning(f"Using fallback for {fetcher_method.__name__}")
            return None
