# backtesting/strategies/wyckoff_backtest.py
from typing import List, Dict, Optional, Any
import pandas as pd
from strategies.wyckoff import WyckoffAccumulationStrategy


class WyckoffBacktester:
    def __init__(self):
        self.strategy = WyckoffAccumulationStrategy()

    def backtest(self, historical_data, lookback=30):
        results = []

        for i in range(lookback, len(historical_data)):
            window = historical_data.iloc[i-lookback:i]
            signal = self.strategy.analyze(window)

            if signal:
                trade = self._simulate_trade(
                    historical_data.iloc[i:],
                    signal
                )
                if trade:
                    results.append(trade)

        return pd.DataFrame(results)

    def _simulate_trade(self, data, signal):
        entry_condition = data['high'] >= signal['entry']
        exit_condition = (data['low'] <= signal['sl']) | (
            data['high'] >= signal['target'])

        if not entry_condition.any():
            return None

        entry_idx = entry_condition.idxmax()
        exit_idx = exit_condition[entry_idx:].idxmax()

        return {
            'entry_date': data.loc[entry_idx]['date'],
            'exit_date': data.loc[exit_idx]['date'],
            'entry_price': signal['entry'],
            'exit_price': (signal['sl'] if data.loc[exit_idx]['low'] <= signal['sl']
                           else signal['target']),
            'type': 'wyckoff_accumulation'
        }

# method 3 final version


class WyckoffBacktester:
    """
    Backtester for the Wyckoff Accumulation Strategy.
    """

    def __init__(self):
        self.strategy = WyckoffAccumulationStrategy()

    def backtest(
        self,
        historical_data: pd.DataFrame,
        lookback: int = 30
    ) -> pd.DataFrame:
        """
        Run backtest on historical data using the Wyckoff Accumulation Strategy.

        Args:
            historical_data (pd.DataFrame): DataFrame with columns ['date', 'open', 'high', 'low', 'close', ...].
            lookback (int): Number of periods to use for each strategy analysis window.

        Returns:
            pd.DataFrame: DataFrame of trade results.
        """
        if not isinstance(historical_data, pd.DataFrame):
            raise ValueError("historical_data must be a pandas DataFrame.")

        required_columns = {'date', 'high', 'low'}
        if not required_columns.issubset(historical_data.columns):
            raise ValueError(
                f"historical_data must contain columns: {required_columns}")

        results: List[Dict[str, Any]] = []

        for i in range(lookback, len(historical_data)):
            window = historical_data.iloc[i - lookback:i]
            signal = self.strategy.analyze(window)

            if signal:
                trade = self._simulate_trade(
                    historical_data.iloc[i:],
                    signal
                )
                if trade:
                    results.append(trade)

        return pd.DataFrame(results)

    def _simulate_trade(
        self,
        data: pd.DataFrame,
        signal: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Simulate a trade based on the signal and subsequent data.

        Args:
            data (pd.DataFrame): DataFrame starting from the signal date.
            signal (dict): Signal dict with 'entry', 'sl', 'target' keys.

        Returns:
            dict or None: Trade result or None if entry never triggered.
        """
        entry_condition = data['high'] >= signal['entry']
        if not entry_condition.any():
            return None

        entry_idx = entry_condition.idxmax()
        # Only consider data from entry onward for exit
        exit_data = data.loc[entry_idx:]
        exit_condition = (exit_data['low'] <= signal['sl']) | (
            exit_data['high'] >= signal['target'])

        if not exit_condition.any():
            # No exit condition met; treat as open trade or skip
            return None

        exit_idx = exit_condition.idxmax()
        exit_row = exit_data.loc[exit_idx]

        exit_price = (
            signal['sl'] if exit_row['low'] <= signal['sl']
            else signal['target']
        )

        return {
            'entry_date': data.loc[entry_idx]['date'],
            'exit_date': exit_row['date'],
            'entry_price': signal['entry'],
            'exit_price': exit_price,
            'type': 'wyckoff_accumulation'
        }
