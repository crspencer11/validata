import pytest
from src.rules import PriceSpikeRule, MonotonicTimeRule

def test_price_spike_rule_perfect_data():
    rule = PriceSpikeRule(threshold_percent=0.10)
    data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": 105},
        {"timestamp": "2023-01-01T02:00:00Z", "price": 110},
    ]
    violations = rule.validate(data)
    assert violations == []

def test_price_spike_rule_garbage_data():
    rule = PriceSpikeRule(threshold_percent=0.10)
    data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": 120},  # Spike
        {"timestamp": "2023-01-01T02:00:00Z", "price": 115},
    ]
    violations = rule.validate(data)
    assert len(violations) == 1
    assert violations[0]["type"] == "PRICE_SPIKE"

def test_monotonic_time_rule_perfect_data():
    rule = MonotonicTimeRule()
    data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": 105},
        {"timestamp": "2023-01-01T02:00:00Z", "price": 110},
    ]
    violations = rule.validate(data)
    assert violations == []

def test_monotonic_time_rule_garbage_data():
    rule = MonotonicTimeRule()
    data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T00:00:00Z", "price": 105},  # Non-sequential
        {"timestamp": "2023-01-01T02:00:00Z", "price": 110},
    ]
    violations = rule.validate(data)
    assert len(violations) == 1
    assert violations[0]["type"] == "TIME_ORDER_ERROR"