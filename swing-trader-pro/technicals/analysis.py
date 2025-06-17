# technicals/analysis.py
import pandas as pd


class Technicals:
    @staticmethod
    def support_break(symbol):
        # Implementation would check technical support
        return False

# method 2 final version
# technicals/analysis.py


class Technicals:
    @staticmethod
    def support_break(symbol, lookback: int = 20, data_provider=None) -> bool:
        """
        Check if the latest close has broken below recent support.

        Args:
            symbol (str): The trading symbol.
            lookback (int): Number of bars to look back for support calculation.
            data_provider (callable, optional): Function to fetch historical data.
                Should accept a symbol and return a DataFrame with 'close' column.

        Returns:
            bool: True if support is broken, False otherwise.
        """
        # Default data provider using yfinance if none supplied
        if data_provider is None:
            try:
                import yfinance as yf
                df = yf.download(symbol, period="2mo",
                                 interval="1d", progress=False)
                if df.empty or 'Close' not in df:
                    return False
                closes = df['Close']
            except Exception as e:
                print(f"[Technicals] Error fetching data for {symbol}: {e}")
                return False
        else:
            df = data_provider(symbol)
            if df is None or 'close' not in df or len(df) < lookback + 1:
                return False
            closes = df['close']

        if len(closes) < lookback + 1:
            return False

        # Support is the minimum of the previous 'lookback' closes (excluding the latest)
        recent_support = closes[-(lookback+1):-1].min()
        latest_close = closes.iloc[-1] if isinstance(
            closes, pd.Series) else closes[-1]

        return latest_close < recent_support
