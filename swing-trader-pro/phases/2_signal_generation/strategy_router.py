# phases/2_signal_generation/strategy_router.py
import logging
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

# method 3 final version


logger = logging.getLogger(__name__)


class StrategyRouter:
    """
    Routes symbol data to all strategies, but for 'institutional' strategy,
    runs HedgeDetector first and only proceeds if no strong hedge is detected.
    """

    def __init__(self):
        self.strategies = {
            'institutional': InstitutionalStrategy(),
            'wyckoff': WyckoffStrategy(),
            'quant': QuantitativeStrategy()
        }
        self.hedge_detector = HedgeDetector()

    def generate_signals(self, symbol_data):
        """
        Generate signals from all strategies.
        For 'institutional', only generate if hedge check passes.
        """
        signals = {}

        # Institutional strategy with hedge check
        try:
            hedge_status = self.hedge_detector.detect_hedges(
                symbol_data.get('symbol'),
                symbol_data.get('fii_flows'),
                symbol_data.get('oi_changes')
            )
            if not all(hedge_status.values()):
                signals['institutional'] = self.strategies['institutional'].analyze(
                    symbol_data)
            else:
                logger.info(
                    f"Hedge detected for {symbol_data.get('symbol')}, skipping institutional strategy.")
        except Exception as e:
            logger.error(f"Error in institutional hedge check: {str(e)}")

        # Other strategies
        for name in ['wyckoff', 'quant']:
            try:
                signals[name] = self.strategies[name].analyze(symbol_data)
            except Exception as e:
                logger.error(f"Error in {name} strategy: {str(e)}")
                continue

        return signals
