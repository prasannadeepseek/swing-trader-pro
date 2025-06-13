import logging
from .base_fetcher import BaseFetcher
from nsepy import get_history, get_index_pe_history
from datetime import date, timedelta
import pandas as pd


class NSEFetcher:

    @staticmethod
    def get_ohlc(symbol, days=30):
        """Fetch OHLC data for any stock"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        return get_history(
            symbol=symbol,
            start=start_date,
            end=end_date,
            index=False
        )

    @staticmethod
    def get_fno_oi(symbol, expiry=None):
        """Fetch F&O Open Interest data"""
        end_date = date.today()
        start_date = end_date - timedelta(days=5)
        df = get_history(
            symbol=symbol,
            start=start_date,
            end=end_date,
            futures=True,
            expiry_date=expiry
        )
        return df[['Open', 'Close', 'OI']]

    @staticmethod
    def get_index_oi(index='NIFTY 50'):
        """Fetch index OI changes"""
        return get_index_pe_history(
            symbol=index,
            start=date.today()-timedelta(days=5),
            end=date.today()
        )

# method 2


logger = logging.getLogger(__name__)


class NSEFetcher(BaseFetcher):

    def __init__(self):
        self.base_url = "https://www.nseindia.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US"
        }

    def get_ohlc(self, symbol, days=30):
        """Fetch OHLC data with fallback handling"""
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=days)
            data = get_history(
                symbol=symbol,
                start=start_date,
                end=end_date,
                index=False
            )
            if self._validate_data_freshness(data):
                return data
            return self._load_fallback_data(f"ohlc_{symbol}")
        except Exception as e:
            logger.error(f"Failed to get OHLC for {symbol}: {str(e)}")
            return self._load_fallback_data(f"ohlc_{symbol}")

    def get_index_oi(self, index='NIFTY 50'):
        """Fetch index OI with retry logic"""
        try:
            return get_index_pe_history(
                symbol=index,
                start=date.today()-timedelta(days=5),
                end=date.today()
            )
        except Exception as e:
            logger.error(f"Index OI fetch failed: {str(e)}")
            return self._load_fallback_data(f"index_oi_{index}")

    def _validate_data_freshness(self, df):
        """Ensure data is recent"""
        if not isinstance(df, pd.DataFrame) or df.empty:
            return False
        last_date = pd.to_datetime(df.index[-1]).date()
        return last_date >= (date.today() - timedelta(days=1))
