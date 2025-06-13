# phases/2_signal_generation/strategy_router.py
from strategies.institutional import (
    InstitutionalFlowStrategy,
    HedgeDetector
)
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

# method 2
# phases/2_signal_generation/strategy_router.py


class StrategyRouter:
    def __init__(self):
        self.strategies = {
            'institutional': InstitutionalFlowStrategy(),
            'hedge_check': HedgeDetector()
        }

    def generate_signals(self, symbol_data):
        """Generate signals with hedge awareness"""
        signals = {}

        # First check for hedging
        hedge_status = self.strategies['hedge_check'].detect_hedges(
            symbol_data['symbol'],
            symbol_data['fii_flows'],
            symbol_data['oi_changes']
        )

        # Only proceed if no strong hedging
        if not all(hedge_status.values()):
            signals['institutional'] = self.strategies['institutional'].analyze(
                symbol_data)

        return signals
