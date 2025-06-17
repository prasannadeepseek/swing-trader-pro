# backtesting/engine/walkforward.py
from typing import Any, Dict, List, Optional, Union
import pandas as pd
from datetime import timedelta


class WalkforwardTester:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data

    def run_test(self, initial_period=180, test_period=30):
        """Run walkforward backtest"""
        results = []
        start_idx = 0

        while start_idx + initial_period + test_period <= len(self.data):
            # Split into training and test sets
            train_data = self.data.iloc[start_idx:start_idx+initial_period]
            test_data = self.data.iloc[start_idx +
                                       initial_period:start_idx+initial_period+test_period]

            # Optimize on training period
            optimized_params = self.strategy.optimize(train_data)

            # Test on out-of-sample period
            test_result = self.strategy.backtest(test_data, optimized_params)
            results.append(test_result)

            # Move window forward
            start_idx += test_period

        return self.analyze_results(results)

    def analyze_results(self, results):
        """Aggregate backtest results"""
        return {
            'win_rate': sum(r['pnl'] > 0 for r in results) / len(results),
            'avg_return': sum(r['pnl'] for r in results) / len(results),
            'max_drawdown': min(r['drawdown'] for r in results)
        }
# method 2


class SwingWalkforward:
    def test_strategy(self, strategy, start_date, end_date):
        results = []
        current = start_date

        while current <= end_date:
            # Simulate weekly cycle
            week_result = self._simulate_week(strategy, current)
            results.append(week_result)
            current += timedelta(weeks=1)

        return self._analyze(results)

# method 3 final versino


class WalkforwardTester:
    """
    Walkforward backtesting engine supporting:
    - Index-based walkforward (rolling window)
    - Date-based walkforward (e.g., weekly stepping)
    - Weekly simulation (from SwingWalkforward)
    """

    def __init__(self, strategy, data: pd.DataFrame):
        """
        Args:
            strategy: Strategy object with optimize() and backtest() methods.
            data (pd.DataFrame): Historical data for backtesting.
        """
        self.strategy = strategy
        self.data = data

    def run_index_walkforward(
        self,
        initial_period: int = 180,
        test_period: int = 30
    ) -> Dict[str, Any]:
        """
        Run index-based walkforward backtest.

        Args:
            initial_period (int): Number of rows for training window.
            test_period (int): Number of rows for test window.

        Returns:
            dict: Aggregated backtest results.
        """
        results = []
        start_idx = 0

        while start_idx + initial_period + test_period <= len(self.data):
            train_data = self.data.iloc[start_idx:start_idx + initial_period]
            test_data = self.data.iloc[start_idx +
                                       initial_period:start_idx + initial_period + test_period]

            optimized_params = self.strategy.optimize(train_data)
            test_result = self.strategy.backtest(test_data, optimized_params)
            results.append(test_result)

            start_idx += test_period

        return self.analyze_results(results)

    def run_date_walkforward(
        self,
        start_date: Union[str, pd.Timestamp],
        end_date: Union[str, pd.Timestamp],
        freq: str = 'W'
    ) -> Dict[str, Any]:
        """
        Run date-based walkforward backtest (e.g., weekly cycles).

        Args:
            start_date (str or pd.Timestamp): Start date for walkforward.
            end_date (str or pd.Timestamp): End date for walkforward.
            freq (str): Frequency string for window stepping (default 'W' for weekly).

        Returns:
            dict: Aggregated backtest results.
        """
        results = []
        current = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        while current <= end_date:
            period_end = current + pd.Timedelta(freq)
            period_data = self.data[self.data.index.to_series().between(
                current, period_end)]
            if not period_data.empty:
                period_result = self._simulate_period(
                    self.strategy, period_data)
                results.append(period_result)
            current = period_end

        return self.analyze_results(results)

    def run_weekly_simulation(
        self,
        start_date: Union[str, pd.Timestamp],
        end_date: Union[str, pd.Timestamp]
    ) -> Dict[str, Any]:
        """
        Simulate weekly cycles, as in the original SwingWalkforward.

        Args:
            start_date (str or pd.Timestamp): Start date for simulation.
            end_date (str or pd.Timestamp): End date for simulation.

        Returns:
            dict: Aggregated backtest results.
        """
        results = []
        current = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        while current <= end_date:
            week_result = self._simulate_week(self.strategy, current)
            results.append(week_result)
            current += timedelta(weeks=1)

        return self.analyze_results(results)

    def _simulate_period(self, strategy, period_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Simulate a single period (e.g., week) for date-based walkforward.

        Args:
            strategy: Strategy object.
            period_data (pd.DataFrame): Data for the period.

        Returns:
            dict: Backtest result for the period.
        """
        # For date-based, we assume no optimization, just backtest
        return strategy.backtest(period_data)

    def _simulate_week(self, strategy, week_start: pd.Timestamp) -> Dict[str, Any]:
        """
        Simulate a single week for the weekly simulation.

        Args:
            strategy: Strategy object.
            week_start (pd.Timestamp): Start date of the week.

        Returns:
            dict: Backtest result for the week.
        """
        week_end = week_start + timedelta(weeks=1)
        week_data = self.data[self.data.index.to_series().between(
            week_start, week_end)]
        if week_data.empty:
            return {'pnl': 0, 'drawdown': 0}
        return strategy.backtest(week_data)

    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate backtest results.

        Args:
            results (list): List of result dicts from backtests.

        Returns:
            dict: Aggregated statistics.
        """
        if not results:
            return {'win_rate': None, 'avg_return': None, 'max_drawdown': None}

        pnl_list = [r.get('pnl', 0) for r in results]
        drawdown_list = [r.get('drawdown', 0) for r in results]

        win_rate = sum(p > 0 for p in pnl_list) / \
            len(pnl_list) if pnl_list else None
        avg_return = sum(pnl_list) / len(pnl_list) if pnl_list else None
        max_drawdown = min(drawdown_list) if drawdown_list else None

        return {
            'win_rate': win_rate,
            'avg_return': avg_return,
            'max_drawdown': max_drawdown
        }
