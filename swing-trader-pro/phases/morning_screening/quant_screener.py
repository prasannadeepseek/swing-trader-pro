# phases/1_morning_screening/quant_screener.py
from typing import Dict, Any, Callable, List, Optional
import talib
import pandas as pd


class QuantitativeScreener:
    def screen(self, universe):
        """Screen stocks based on quantitative factors"""
        screened = {}

        for symbol in universe:
            data = self._get_symbol_data(symbol)

            # Momentum filter
            rsi = talib.RSI(data['close'], timeperiod=14)[-1]
            mom_filter = 30 < rsi < 70

            # Volume filter
            volume_ma = talib.SMA(data['volume'], timeperiod=20)[-1]
            vol_filter = data['volume'][-1] > 1.5 * volume_ma

            if mom_filter and vol_filter:
                screened[symbol] = {
                    'rsi': rsi,
                    'volume_ratio': data['volume'][-1] / volume_ma
                }

        return screened

# method 2 final version


class QuantitativeScreener:
    """
    Screens stocks based on quantitative factors such as RSI and volume.
    Allows for custom data fetching and flexible screening logic.
    """

    def __init__(self, data_fetcher: Optional[Callable[[str], pd.DataFrame]] = None):
        """
        Args:
            data_fetcher (callable, optional): Function to fetch symbol data. 
                Should accept a symbol and return a DataFrame with 'close' and 'volume' columns.
        """
        self.data_fetcher = data_fetcher or self._get_symbol_data

    def screen(self, universe: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Screen stocks based on quantitative factors (RSI and volume).

        Args:
            universe (list): List of stock symbols.

        Returns:
            dict: Symbols passing the screen with their metrics.
        """
        screened = {}

        for symbol in universe:
            try:
                data = self.data_fetcher(symbol)
                if data is None or len(data) < 20:
                    continue

                # Momentum filter
                rsi = talib.RSI(data['close'], timeperiod=14)[-1]
                mom_filter = 30 < rsi < 70

                # Volume filter
                volume_ma = talib.SMA(data['volume'], timeperiod=20)[-1]
                vol_filter = data['volume'][-1] > 1.5 * volume_ma

                if mom_filter and vol_filter:
                    screened[symbol] = {
                        'rsi': rsi,
                        'volume_ratio': data['volume'][-1] / volume_ma
                    }
            except Exception as e:
                print(f"[QuantitativeScreener] Error screening {symbol}: {e}")

        return screened

    def _get_symbol_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Placeholder for fetching symbol data. Should be replaced with actual data source.

        Args:
            symbol (str): The stock symbol.

        Returns:
            pd.DataFrame or None: DataFrame with 'close' and 'volume' columns.
        """
        # TODO: Implement actual data fetching logic
        return None

# method 2 final version with complete todo


class QuantitativeScreener:
    """
    Screens stocks based on quantitative factors such as RSI and volume.
    Allows for custom data fetching and flexible screening logic.
    """

    def __init__(self, data_fetcher: Optional[Callable[[str], pd.DataFrame]] = None):
        """
        Args:
            data_fetcher (callable, optional): Function to fetch symbol data. 
                Should accept a symbol and return a DataFrame with 'close' and 'volume' columns.
        """
        self.data_fetcher = data_fetcher or self._get_symbol_data

    def screen(self, universe: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Screen stocks based on quantitative factors (RSI and volume).

        Args:
            universe (list): List of stock symbols.

        Returns:
            dict: Symbols passing the screen with their metrics.
        """
        screened = {}

        for symbol in universe:
            try:
                data = self.data_fetcher(symbol)
                if data is None or len(data) < 20:
                    continue

                # Momentum filter
                rsi = talib.RSI(data['close'], timeperiod=14)[-1]
                mom_filter = 30 < rsi < 70

                # Volume filter
                volume_ma = talib.SMA(data['volume'], timeperiod=20)[-1]
                vol_filter = data['volume'][-1] > 1.5 * volume_ma

                if mom_filter and vol_filter:
                    screened[symbol] = {
                        'rsi': rsi,
                        'volume_ratio': data['volume'][-1] / volume_ma
                    }
            except Exception as e:
                print(f"[QuantitativeScreener] Error screening {symbol}: {e}")

        return screened

    def _get_symbol_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Fetch historical OHLCV data for a symbol using yfinance.

        Args:
            symbol (str): The stock symbol.

        Returns:
            pd.DataFrame or None: DataFrame with 'close' and 'volume' columns.
        """
        try:
            import yfinance as yf
            # Adjust symbol for Yahoo Finance if needed (e.g., NSE stocks: 'RELIANCE.NS')
            yf_symbol = symbol if '.' in symbol else f"{symbol}.NS"
            df = yf.download(yf_symbol, period="2mo",
                             interval="1d", progress=False)
            if df.empty or 'Close' not in df or 'Volume' not in df:
                return None
            # Standardize column names
            df = df.rename(columns={'Close': 'close', 'Volume': 'volume'})
            return df[['close', 'volume']].dropna()
        except Exception as e:
            print(
                f"[QuantitativeScreener] Error fetching data for {symbol}: {e}")
            return None
