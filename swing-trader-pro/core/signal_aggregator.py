# core/signal_aggregator.py
from typing import Dict, Any
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

# method 2 final version


class SignalAggregator:
    """
    Aggregates signals from multiple strategies using weighted scores.

    Expected input format for `signals`:
        {
            'strategy_name': {
                'SYMBOL1': {'score': float, ...},
                'SYMBOL2': {'score': float, ...},
                ...
            },
            ...
        }
    """

    def __init__(self):
        self.strategy_weights = {
            'institutional': 0.4,
            'wyckoff': 0.3,
            'quant': 0.3
        }

    def aggregate_signals(self, signals: Dict[str, Dict[str, dict]]) -> Dict[str, Any]:
        """
        Combine signals from multiple strategies into a composite score per symbol.

        Args:
            signals: Dict mapping strategy name to dict of symbol: signal dict.

        Returns:
            Dict mapping symbol to {
                'composite_score': float,
                'signals': list of signal dicts from all strategies for that symbol
            }
        """
        if not signals:
            return {}

        aggregated = {}

        # Collect all unique symbols across all strategies
        all_symbols = set()
        for strategy_signals in signals.values():
            if not isinstance(strategy_signals, dict):
                continue
            all_symbols.update(strategy_signals.keys())

        for symbol in sorted(all_symbols):
            symbol_scores = []
            symbol_signals = []

            for strategy, strategy_signals in signals.items():
                if not isinstance(strategy_signals, dict):
                    continue
                if symbol in strategy_signals:
                    score = strategy_signals[symbol].get('score', 0)
                    weight = self.strategy_weights.get(strategy, 0)
                    weighted_score = score * weight
                    symbol_scores.append(weighted_score)
                    symbol_signals.append(strategy_signals[symbol])

            if symbol_scores:
                aggregated[symbol] = {
                    'composite_score': sum(symbol_scores),
                    'signals': symbol_signals
                }

        return aggregated
