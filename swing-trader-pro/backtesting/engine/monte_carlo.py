# backtesting/engine/monte_carlo.py
import numpy as np


class MonteCarloSimulator:
    def __init__(self, returns_series):
        self.returns = returns_series

    def run_simulation(self, n_sims=1000, periods=252):
        """Run Monte Carlo simulation"""
        sims = np.zeros((n_sims, periods))
        mean, vol = self.returns.mean(), self.returns.std()

        for i in range(n_sims):
            sims[i] = np.random.normal(
                loc=mean,
                scale=vol,
                size=periods
            ).cumsum()

        return {
            'median': np.median(sims[:, -1]),
            'top_5%': np.percentile(sims[:, -1], 95),
            'bottom_5%': np.percentile(sims[:, -1], 5)
        }
