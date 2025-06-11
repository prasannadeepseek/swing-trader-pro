# backtesting/strategies/institutional_backtest.py
import pandas as pd
from strategies.institutional import InstitutionalFlowStrategy


class InstitutionalBacktester:
    def __init__(self):
        self.strategy = InstitutionalFlowStrategy()

    def backtest(self, historical_data):
        results = []

        for date, day_data in historical_data.groupby(pd.Grouper(key='date', freq='D')):
            signal = self.strategy.analyze(day_data.iloc[-1])
            if signal:
                trade = self._simulate_trade(day_data, signal)
                results.append(trade)

        return pd.DataFrame(results)

    def _simulate_trade(self, data, signal):
        entry_idx = data.index.get_loc(data.index[-1]) + 1
        exit_idx = min(entry_idx + signal['validity_days'], len(data)-1)

        entry_price = data.iloc[entry_idx]['open']
        exit_price = data.iloc[exit_idx]['close']

        return {
            'entry_date': data.iloc[entry_idx]['date'],
            'exit_date': data.iloc[exit_idx]['date'],
            'pnl': exit_price - entry_price,
            'pnl_pct': (exit_price - entry_price) / entry_price
        }
