#!/bin/bash
# scripts/morning_setup.py
import os
from core.data_pipeline import DataPipeline

if __name__ == "__main__":
    print("Running morning setup...")
    DataPipeline().prefetch_universe()
    print("Setup complete!")
# method 2 un finised version
import logging
from datetime import datetime, timedelta
import pandas as pd

# ... (other imports and class code remain unchanged)


class DataPipeline:
    """
    Unified DataPipeline class combining broker integration, error handling,
    logging, fallback logic, and modular fetchers.
    """

    def __init__(self, broker_api=None):
        # Initialize fetchers
        self.nse = NSEFetcher()
        self.nsdl = NSDLFetcher()
        self.block = BlockDealFetcher()
        self._last_fetch_time = {}

        # Broker integration (optional)
        self.broker = BrokerDataFetcher(**broker_api) if broker_api else None

        # API endpoints for generic fetches (if needed)
        self.sources = {
            'price': 'https://marketdata.api/price',
            'volume': 'https://marketdata.api/volume',
            'fii_cash': 'https://nsdl.com/fii_cash',
            'fii_derivatives': 'https://nsdl.com/fii_fno',
            'block_deals': 'https://nseindia.com/block_deals',
            'oi_data': 'https://nseindia.com/oi'
        }

    # ... (existing methods unchanged)

    def prefetch_universe(self, universe=None, days=30):
        """
        Prefetch and cache all relevant data for the trading universe.
        Args:
            universe (list, optional): List of symbols to prefetch. If None, uses default universe.
            days (int): Number of days of historical data to fetch.
        """
        logger = logging.getLogger("DataPipeline")
        logger.info("Starting prefetch for trading universe...")

        if universe is None:
            # Example: Replace with actual universe fetch logic
            universe = self._get_default_universe()

        for symbol in universe:
            try:
                logger.info(f"Prefetching data for {symbol}...")
                self.get_institutional_data(symbol, days=days)
                self.fetch_data(symbol, days=days)
            except Exception as e:
                logger.error(f"Prefetch failed for {symbol}: {e}")

        logger.info("Prefetch complete for all symbols.")

    def _get_default_universe(self):
        """
        Returns the default trading universe.
        Replace this with actual logic to fetch your universe.
        """
        # Example: NIFTY 50 symbols
        return [
            "RELIANCE", "HDFCBANK", "INFY", "ICICIBANK", "TCS", "HINDUNILVR",
            "SBIN", "BHARTIARTL", "KOTAKBANK", "LT"
        ]

# methid 2


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    logger = logging.getLogger("MorningSetup")
    logger.info("Running morning setup...")

    try:
        pipeline = DataPipeline()
        pipeline.prefetch_universe()
        logger.info("Setup complete!")
    except Exception as e:
        logger.exception(f"Morning setup failed: {e}")


if __name__ == "__main__":
    main()
