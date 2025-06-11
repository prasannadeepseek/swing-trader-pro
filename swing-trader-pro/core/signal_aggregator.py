# core/signal_aggregator.py
from typing import Dict, List


class SignalAggregator:
    def __init__(self):
        self.strategy_weights = {
            'institutional': 0.4,
            'wyckoff': 0.3,
            'quant': 0.3
        }

    def aggregate_signals(self, signals: Dict[str, List[dict]]) -> dict:
        """Combine signals from multiple strategies"""
        aggregated = {}

        for symbol in set().union(*[s.keys() for s in signals.values()]):
            symbol_scores = []

            for strategy, strategy_signals in signals.items():
                if symbol in strategy_signals:
                    weighted_score = (
                        strategy_signals[symbol]['score'] *
                        self.strategy_weights[strategy]
                    )
                    symbol_scores.append(weighted_score)

            if symbol_scores:
                aggregated[symbol] = {
                    'composite_score': sum(symbol_scores),
                    'signals': [s[symbol] for s in signals.values()
                                if symbol in s]
                }

        return aggregated
