"""
Unit Tests for Panta Oracle Agent
Verifies Bayesian probability estimation, EV detection, and Kelly Criterion calculations.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oracle_brain import OracleBrain, PredictionMarket

def test_implied_probability():
    m = PredictionMarket(
        id="test_1",
        title="Will Solana TPS exceed 5,000?",
        category="Tech",
        yes_price=0.60,
        no_price=0.40,
        volume_usdc=50000.0,
        end_date="2026-11-01",
        resolution_source="SolanaFM"
    )
    assert round(m.implied_yes_prob, 2) == 0.60
    assert round(m.implied_no_prob, 2) == 0.40

def test_positive_ev_detection():
    brain = OracleBrain(min_ev_threshold=0.10)
    m = PredictionMarket(
        id="test_2",
        title="Will SOL close above $200?",
        category="Crypto",
        yes_price=0.40,  # market gives 40%
        no_price=0.60,
        volume_usdc=10000.0,
        end_date="2026-11-01",
        resolution_source="Pyth"
    )
    # Fair prob is 60% -> EV = 0.60 / 0.40 - 1 = +50%
    analysis = brain.evaluate_market(m, fair_yes_prob=0.60, bankroll_usdc=1000.0)
    assert analysis.recommended_side == "YES"
    assert round(analysis.expected_value, 2) == 0.50
    assert round(analysis.edge_pct, 1) == 20.0
    assert analysis.recommended_size_usdc > 0.0

def test_negative_ev_rejection():
    brain = OracleBrain(min_ev_threshold=0.10)
    m = PredictionMarket(
        id="test_3",
        title="Fair Coin Flip",
        category="Game",
        yes_price=0.52,  # Overpriced
        no_price=0.52,
        volume_usdc=1000.0,
        end_date="2026-11-01",
        resolution_source="Oracle"
    )
    analysis = brain.evaluate_market(m, fair_yes_prob=0.50, bankroll_usdc=1000.0)
    assert analysis.expected_value < 0.10

def test_kelly_criterion_bounds():
    brain = OracleBrain(min_ev_threshold=0.05, max_kelly_fraction=0.25)
    m = PredictionMarket(
        id="test_4",
        title="High Conviction Trade",
        category="Solana",
        yes_price=0.30,
        no_price=0.70,
        volume_usdc=20000.0,
        end_date="2026-11-01",
        resolution_source="Pyth"
    )
    analysis = brain.evaluate_market(m, fair_yes_prob=0.70, bankroll_usdc=1000.0)
    # Ensure fractional Kelly never risks more than safe limit (15% of bankroll)
    assert analysis.kelly_stake_fraction <= 0.15
    assert analysis.recommended_size_usdc <= 150.0

if __name__ == "__main__":
    test_implied_probability()
    test_positive_ev_detection()
    test_negative_ev_rejection()
    test_kelly_criterion_bounds()
    print("✅ All Panta Oracle Agent unit tests passed successfully!")
