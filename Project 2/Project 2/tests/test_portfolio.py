"""Small reproducibility checks for the portfolio engine."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from portfolio import (  # noqa: E402
    CORRELATION,
    SLEEVES,
    benchmark_weights,
    covariance_matrix,
    equal_weight_weights,
    expected_return,
    portfolio_volatility,
    search_lowest_risk_mix,
)


class PortfolioEngineTests(unittest.TestCase):
    def setUp(self):
        self.covariance = covariance_matrix(SLEEVES, CORRELATION)

    def test_training_benchmark_known_answer(self):
        weights = benchmark_weights(SLEEVES)
        self.assertAlmostEqual(expected_return(weights, SLEEVES), 0.0680, places=6)
        self.assertAlmostEqual(
            portfolio_volatility(weights, self.covariance, SLEEVES), 0.1046, places=4
        )

    def test_training_equal_weight_known_answer(self):
        weights = equal_weight_weights(SLEEVES)
        self.assertAlmostEqual(expected_return(weights, SLEEVES), 0.0520, places=6)
        self.assertAlmostEqual(
            portfolio_volatility(weights, self.covariance, SLEEVES), 0.0521, places=4
        )

    def test_unreachable_return_has_no_solution(self):
        result = search_lowest_risk_mix(SLEEVES, CORRELATION, objective_return=0.20)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
