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
