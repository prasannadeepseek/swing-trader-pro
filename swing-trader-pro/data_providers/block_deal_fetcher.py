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

# method 3 final version


logger = logging.getLogger(__name__)


class BlockDealFetcher(BaseFetcher):
    """
    Fetches and processes block deals from NSE, with error handling, fallback, and FII filtering.
    """

    NSE_API = "https://www.nseindia.com/api/block-deals"

    def get_recent_block_deals(self, days=1, filter_fii=True):
        """
        Fetch recent block deals from NSE, optionally filtering for FII activity.

        Args:
            days (int): Number of days to look back for deals.
            filter_fii (bool): If True, only include deals with FII in client name.

        Returns:
            pd.DataFrame: DataFrame of filtered block deals.
        """
        try:
            response = self._fetch_url(
                self.NSE_API,
                headers={"User-Agent": "Mozilla/5.0",
                         "Accept-Language": "en-US"}
            )
            deals = response.json()
            filtered_deals = self._parse_and_filter_deals(
                deals, days, filter_fii)
            return pd.DataFrame(filtered_deals)
        except Exception as e:
            logger.error(f"Block deal fetch failed: {str(e)}")
            fallback = self._load_fallback_data("block_deals")
            if fallback is not None:
                try:
                    deals = fallback.json()
                    filtered_deals = self._parse_and_filter_deals(
                        deals, days, filter_fii)
                    return pd.DataFrame(filtered_deals)
                except Exception as fallback_e:
                    logger.error(
                        f"Fallback block deal parse failed: {fallback_e}")
            return pd.DataFrame([])

    def _parse_and_filter_deals(self, deals, days, filter_fii):
        """
        Parse and filter deals for recency and FII activity.

        Args:
            deals (list): List of deal dicts from API.
            days (int): Number of days to look back.
            filter_fii (bool): If True, only include FII deals.

        Returns:
            list: List of filtered deal dicts.
        """
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
        filtered = []
        for deal in deals:
            try:
                trade_date = pd.to_datetime(
                    deal.get('tradeDate'), format='%d-%b-%Y', errors='coerce')
                if pd.isnull(trade_date) or trade_date < cutoff:
                    continue
                client_name = deal.get('clientName', '').upper()
                if filter_fii and 'FII' not in client_name:
                    continue
                filtered.append({
                    'symbol': deal.get('symbol'),
                    'qty': deal.get('quantity'),
                    'price': deal.get('price'),
                    'date': trade_date,
                    'clientName': deal.get('clientName')
                })
            except Exception as e:
                logger.warning(f"Skipping deal due to parse error: {e}")
        return filtered
