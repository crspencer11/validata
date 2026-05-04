from src.engine import DataValidator
from src.rules import PriceSpikeRule, MonotonicTimeRule

def test_data_validator_perfect_data():
    rules = [PriceSpikeRule(threshold_percent=0.10), MonotonicTimeRule()]
    validator = DataValidator(rules=rules)
    
    perfect_data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": 101},
        {"timestamp": "2023-01-01T02:00:00Z", "price": 102},
    ]
    
    result = validator.run(perfect_data)
    
    assert result["status"] == "PASSED"
    assert result["count"] == 0
    assert result["violations"] == []

def test_data_validator_garbage_data():
    rules = [PriceSpikeRule(threshold_percent=0.10), MonotonicTimeRule()]
    validator = DataValidator(rules=rules)
    
    garbage_data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T00:59:00Z", "price": 120},  # Price spike
        {"timestamp": "2023-01-01T00:58:00Z", "price": 110},  # Out of order
    ]
    
    result = validator.run(garbage_data)
    
    assert result["status"] == "FAILED"
    assert result["count"] > 0
    assert any(violation["type"] == "PRICE_SPIKE" for violation in result["violations"])
    assert any(violation["type"] == "TIME_ORDER_ERROR" for violation in result["violations"])