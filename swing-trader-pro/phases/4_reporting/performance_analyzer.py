# phases/4_reporting/performance_analyzer.py
from typing import List, Dict, Any
import pandas as pd


class PerformanceAnalyzer:
    METRICS = [
        'sharpe_ratio',
        'max_drawdown',
        'win_rate',
        'profit_factor'
    ]

    def analyze(self, trades):
        """Calculate key performance metrics"""
        df = pd.DataFrame(trades)
        df['date'] = pd.to_datetime(df['exit_time'])

        return {
            'sharpe_ratio': self._calculate_sharpe(df),
            'max_drawdown': self._calculate_drawdown(df),
            'win_rate': len(df[df['pnl'] > 0]) / len(df),
            'profit_factor': (
                df[df['pnl'] > 0]['pnl'].sum() /
                abs(df[df['pnl'] < 0]['pnl'].sum())
            )
        }

    def _calculate_sharpe(self, df):
        daily_returns = df.set_index('date')['pnl_pct']
        return (daily_returns.mean() * 252**0.5) / daily_returns.std()

    def _calculate_drawdown(self, df):
        cum_returns = (1 + df.set_index('date')['pnl_pct']).cumprod()
        peak = cum_returns.expanding(min_periods=1).max()
        return (cum_returns / peak - 1).min()

# method 2 final version
# phases/4_reporting/performance_analyzer.py


class PerformanceAnalyzer:
    """
    Analyzes trading performance and computes key metrics such as Sharpe ratio,
    maximum drawdown, win rate, and profit factor.
    """

    METRICS = [
        'sharpe_ratio',
        'max_drawdown',
        'win_rate',
        'profit_factor'
    ]

    def analyze(self, trades: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate key performance metrics from a list of trade dictionaries.

        Args:
            trades (List[Dict]): Each dict should have at least 'exit_time', 'pnl', and 'pnl_pct'.

        Returns:
            Dict[str, float]: Dictionary of computed metrics.
        """
        if not trades:
            return {metric: float('nan') for metric in self.METRICS}

        df = pd.DataFrame(trades)
        if 'exit_time' not in df or 'pnl' not in df or 'pnl_pct' not in df:
            raise ValueError(
                "Each trade must have 'exit_time', 'pnl', and 'pnl_pct' fields.")

        df['date'] = pd.to_datetime(df['exit_time'])

        sharpe = self._calculate_sharpe(df)
        max_dd = self._calculate_drawdown(df)
        win_rate = (len(df[df['pnl'] > 0]) / len(df)
                    ) if len(df) > 0 else float('nan')
        gross_profit = df[df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(df[df['pnl'] < 0]['pnl'].sum())
        profit_factor = (
            gross_profit / gross_loss) if gross_loss > 0 else float('inf')

        return {
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'win_rate': win_rate,
            'profit_factor': profit_factor
        }

    def _calculate_sharpe(self, df: pd.DataFrame) -> float:
        """
        Calculate the annualized Sharpe ratio based on daily returns.

        Args:
            df (pd.DataFrame): DataFrame with 'date' and 'pnl_pct' columns.

        Returns:
            float: Sharpe ratio (annualized).
        """
        daily_returns = df.set_index('date')['pnl_pct']
        if daily_returns.std() == 0 or len(daily_returns) < 2:
            return float('nan')
        return (daily_returns.mean() * (252 ** 0.5)) / daily_returns.std()

    def _calculate_drawdown(self, df: pd.DataFrame) -> float:
        """
        Calculate the maximum drawdown.

        Args:
            df (pd.DataFrame): DataFrame with 'date' and 'pnl_pct' columns.

        Returns:
            float: Maximum drawdown (as a negative percentage).
        """
        cum_returns = (1 + df.set_index('date')['pnl_pct']).cumprod()
        peak = cum_returns.expanding(min_periods=1).max()
        drawdown = (cum_returns / peak - 1)
        return drawdown.min() if not drawdown.empty else float('nan')
