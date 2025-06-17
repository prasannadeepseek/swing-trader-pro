# volume/analysis.py
import pandas as pd


class VolumeAnalysis:
    @staticmethod
    def is_drying(symbol):
        # Implementation would analyze volume
        return False

# method 2 final version
# volume/analysis.py


class VolumeAnalysis:
    @staticmethod
    def is_drying(symbol, lookback: int = 20, threshold: float = 0.5, data_provider=None) -> bool:
        """
        Determine if the recent volume is 'drying up' (significantly below average).

        Args:
            symbol (str): The trading symbol.
            lookback (int): Number of periods for average volume calculation.
            threshold (float): Fraction of average volume to consider as 'drying' (e.g., 0.5 means 50% below average).
            data_provider (callable, optional): Function to fetch historical data.
                Should accept a symbol and return a DataFrame with 'volume' column.

        Returns:
            bool: True if volume is drying up, False otherwise.
        """
        # Default data provider using yfinance if none supplied
        if data_provider is None:
            try:
                import yfinance as yf
                df = yf.download(symbol, period="2mo",
                                 interval="1d", progress=False)
                if df.empty or 'Volume' not in df:
                    return False
                volumes = df['Volume']
            except Exception as e:
                print(
                    f"[VolumeAnalysis] Error fetching data for {symbol}: {e}")
                return False
        else:
            df = data_provider(symbol)
            if df is None or 'volume' not in df or len(df) < lookback + 1:
                return False
            volumes = df['volume']

        if len(volumes) < lookback + 1:
            return False

        avg_volume = volumes[-(lookback+1):-1].mean()
        latest_volume = volumes.iloc[-1] if isinstance(
            volumes, pd.Series) else volumes[-1]

        # If latest volume is less than threshold * average, consider it "drying"
        return latest_volume < threshold * avg_volume
