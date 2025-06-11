# phases/2_signal_generation/strategy_router.py
from strategies import (
    InstitutionalStrategy,
    WyckoffStrategy,
    QuantitativeStrategy
)


class StrategyRouter:
    def __init__(self):
        self.strategies = {
            'institutional': InstitutionalStrategy(),
            'wyckoff': WyckoffStrategy(),
            'quant': QuantitativeStrategy()
        }

    def generate_signals(self, symbol_data):
        """Generate signals from all strategies"""
        signals = {}

        for name, strategy in self.strategies.items():
            try:
                signals[name] = strategy.analyze(symbol_data)
            except Exception as e:
                print(f"Error in {name} strategy: {str(e)}")
                continue

        return signals
