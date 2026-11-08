import pytest
from token_atlas.metrics import (
    calculate_inflation_index,
    calculate_bytes_per_token,
    calculate_effective_context,
    calculate_cost_multiplier,
)


def test_calculate_inflation_index():
    # Exact parity
    assert calculate_inflation_index(100, 100) == 1.0
    # 2.5x inflation
    assert calculate_inflation_index(250, 100) == 2.5
    # Compression (fewer tokens than English)
    assert calculate_inflation_index(80, 100) == 0.8
    # Edge case: 0 baseline tokens
    assert calculate_inflation_index(0, 0) == 1.0
    assert calculate_inflation_index(50, 0) == 50.0


def test_calculate_bytes_per_token():
    # 100 bytes into 25 tokens = 4.0 BPT
    assert calculate_bytes_per_token(100, 25) == 4.0
    # Edge case: 0 tokens
    assert calculate_bytes_per_token(100, 0) == 0.0
    assert calculate_bytes_per_token(0, 50) == 0.0


def test_calculate_effective_context():
    nominal = 128000
    # tau = 1.0 -> 128k
    assert calculate_effective_context(nominal, 1.0) == 128000
    # tau = 2.0 -> 64k
    assert calculate_effective_context(nominal, 2.0) == 64000
    # tau = 3.2 -> 40,000
    assert calculate_effective_context(nominal, 3.2) == 40000
    # Edge case: zero or negative tau
    assert calculate_effective_context(nominal, 0.0) == 128000


def test_calculate_cost_multiplier():
    assert calculate_cost_multiplier(1.0) == 1.0
    assert calculate_cost_multiplier(2.45) == 2.45
    assert calculate_cost_multiplier(-0.5) == 0.0
