# backtesting/engine/walkforward.py
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
# code 2


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
