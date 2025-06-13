import logging
from .base_fetcher import BaseFetcher
import requests
import pandas as pd
from datetime import datetime


class BlockDealFetcher:

    NSE_API = "https://www.nseindia.com/api/block-deals"

    @staticmethod
    def get_recent_block_deals(days=1):
        """Fetch block deals from NSE"""
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US"
        }
        response = requests.get(
            BlockDealFetcher.NSE_API,
            headers=headers
        )
        data = response.json()

        # Filter for FII activity
        fii_deals = []
        for deal in data:
            if 'FII' in deal['clientName'].upper():
                fii_deals.append({
                    'symbol': deal['symbol'],
                    'qty': deal['quantity'],
                    'price': deal['price'],
                    'date': datetime.strptime(deal['tradeDate'], '%d-%b-%Y')
                })
        return pd.DataFrame(fii_deals)

# method 2


logger = logging.getLogger(__name__)


class BlockDealFetcher(BaseFetcher):

    NSE_API = "https://www.nseindia.com/api/block-deals"

    def get_recent_block_deals(self, days=1):
        """Fetch with all safety features"""
        try:
            response = self._fetch_url(
                self.NSE_API,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            deals = self._parse_deals(response.json())
            return self._filter_recent(deals, days)
        except Exception as e:
            logger.error(f"Block deal fetch failed: {str(e)}")
            return self._load_fallback_data("block_deals")

    def _filter_recent(self, deals, days):
        """Filter deals from last N days"""
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
        return [d for d in deals if pd.to_datetime(d['date']) >= cutoff]
