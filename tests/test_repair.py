# tests/test_repair.py — test the rule-based repair instead
from src.rules import PriceSpikeRule, MonotonicTimeRule
import copy

def test_price_spike_repair():
    data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": 250},  # spike
        {"timestamp": "2023-01-01T02:00:00Z", "price": 150},
    ]
    rule = PriceSpikeRule(threshold_percent=0.10, enable_repair=True)
    repaired = rule.repair(copy.deepcopy(data))
    assert repaired[1]["price"] == 175.0  # avg of 250 and 150 (the two neighbors)

def test_time_order_repair():
    data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T00:00:00Z", "price": 110},  # duplicate timestamp
        {"timestamp": "2023-01-01T02:00:00Z", "price": 120},
    ]
    rule = MonotonicTimeRule(enable_repair=True)
    repaired = rule.repair(copy.deepcopy(data))
    assert repaired[1]["timestamp"] > repaired[0]["timestamp"]