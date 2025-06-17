class WeightAllocator:
    RISK_PROFILES = {
        'uptrend': {'base_weight': 0.7, 'sl_multiplier': 1.5},
        'downtrend': {'base_weight': 0.4, 'sl_multiplier': 1.2},
        'consolidation': {'base_weight': 0.5, 'sl_multiplier': 1.3}
    }

    def allocate(self, symbol, analysis):
        profile = self.RISK_PROFILES[analysis['trend_type']]
        return {
            'symbol': symbol,
            'weight': profile['base_weight'] * analysis['composite_score'],
            'trend': analysis['trend_type'],
            'sl_multiplier': profile['sl_multiplier']
        }
# method 2 final version


class WeightAllocator:
    """
    Allocates position weights and stop-loss multipliers based on trend analysis and risk profiles.
    """

    RISK_PROFILES = {
        'uptrend': {'base_weight': 0.7, 'sl_multiplier': 1.5},
        'downtrend': {'base_weight': 0.4, 'sl_multiplier': 1.2},
        'consolidation': {'base_weight': 0.5, 'sl_multiplier': 1.3}
    }

    def allocate(self, symbol: str, analysis: dict) -> dict:
        """
        Allocate weight and stop-loss multiplier for a symbol based on analysis.

        Args:
            symbol (str): The trading symbol.
            analysis (dict): Analysis dict with at least 'trend_type' and 'composite_score'.

        Returns:
            dict: Allocation result with symbol, weight, trend, and sl_multiplier.
        """
        trend_type = analysis.get('trend_type')
        if trend_type not in self.RISK_PROFILES:
            raise ValueError(
                f"Unknown trend_type '{trend_type}' for symbol {symbol}")

        profile = self.RISK_PROFILES[trend_type]
        composite_score = analysis.get('composite_score', 1.0)
        try:
            composite_score = float(composite_score)
        except (TypeError, ValueError):
            composite_score = 1.0

        # Calculate and normalize weight
        raw_weight = profile['base_weight'] * composite_score
        weight = max(0.0, min(raw_weight, 1.0))  # Clamp between 0 and 1

        return {
            'symbol': symbol,
            'weight': weight,
            'trend': trend_type,
            'sl_multiplier': profile['sl_multiplier']
        }
