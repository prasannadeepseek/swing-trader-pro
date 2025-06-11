# phases/4_reporting/performance_analyzer.py
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
