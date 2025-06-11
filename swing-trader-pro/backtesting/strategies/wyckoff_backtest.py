# backtesting/strategies/wyckoff_backtest.py
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
