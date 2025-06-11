# core/data_pipeline.py
import pandas as pd
from datetime import datetime, timedelta


class DataPipeline:
    def __init__(self):
        self.sources = {
            'price': 'https://marketdata.api/price',
            'volume': 'https://marketdata.api/volume'
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
