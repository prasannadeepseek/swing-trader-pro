# backtesting/engine/monte_carlo.py
from typing import Optional, Dict, Any
import pandas as pd
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

# method 2 final versin


class MonteCarloSimulator:
    """
    Monte Carlo Simulator for financial return series.

    Attributes:
        returns (pd.Series): Series of historical returns.
    """

    def __init__(self, returns_series: pd.Series):
        """
        Initialize the MonteCarloSimulator.

        Args:
            returns_series (pd.Series): Series of historical returns.
        """
        self.returns = returns_series

    def run_simulation(
        self,
        n_sims: int = 1000,
        periods: int = 252,
        start_value: float = 0.0,
        random_seed: Optional[int] = None,
        return_paths: bool = False
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation.

        Args:
            n_sims (int): Number of simulations to run.
            periods (int): Number of periods per simulation.
            start_value (float): Starting value for each simulation path.
            random_seed (Optional[int]): Seed for reproducibility.
            return_paths (bool): If True, include all simulation paths in the result.

        Returns:
            Dict[str, Any]: Dictionary with simulation statistics and optionally all paths.
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        sims = np.zeros((n_sims, periods))
        mean, vol = self.returns.mean(), self.returns.std()

        for i in range(n_sims):
            sims[i] = np.random.normal(
                loc=mean,
                scale=vol,
                size=periods
            ).cumsum() + start_value

        results = {
            'median': np.median(sims[:, -1]),
            'top_5%': np.percentile(sims[:, -1], 95),
            'bottom_5%': np.percentile(sims[:, -1], 5)
        }
        if return_paths:
            results['paths'] = sims

        return results
