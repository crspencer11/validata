from src.repair import Repairer

def test_repair_price_spike():
    data_with_spike = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": 250},  # Spike
        {"timestamp": "2023-01-01T02:00:00Z", "price": 150},
    ]
    
    repaired_data = Repairer.repair_price_spike(data_with_spike, threshold_percent=0.10)
    
    assert repaired_data[1]["price"] == 150  # Should be repaired to the average of 100 and 150

def test_repair_missing_prices():
    data_with_missing = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": None},  # Missing price
        {"timestamp": "2023-01-01T02:00:00Z", "price": 150},
    ]
    
    repaired_data = Repairer.repair_missing_prices(data_with_missing)
    
    assert repaired_data[1]["price"] == 125  # Should be repaired to the average of 100 and 150

def test_repair_no_violations():
    perfect_data = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T01:00:00Z", "price": 110},
        {"timestamp": "2023-01-01T02:00:00Z", "price": 120},
    ]
    
    repaired_data = Repairer.repair(perfect_data)
    
    assert repaired_data == perfect_data  # No repairs should be made

def test_repair_time_order():
    data_with_time_error = [
        {"timestamp": "2023-01-01T00:00:00Z", "price": 100},
        {"timestamp": "2023-01-01T00:00:00Z", "price": 110},  # Time error
        {"timestamp": "2023-01-01T02:00:00Z", "price": 120},
    ]
    
    repaired_data = Repairer.repair_time_order(data_with_time_error)
    
    assert repaired_data[1]["timestamp"] > repaired_data[0]["timestamp"]  # Should be repaired to a valid timestamp order