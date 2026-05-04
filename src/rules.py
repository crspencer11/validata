from abc import ABC, abstractmethod
import copy

class ValidationRule(ABC):
    @abstractmethod
    def validate(self, data: list[dict]) -> list[dict]:
        """Returns a list of violation records."""
        pass

    def repair(self, data: list[dict]) -> list[dict]:
        return data
    
import copy

class PriceSpikeRule(ValidationRule):
    def __init__(self, threshold_percent=0.10, enable_repair=False):
        self.threshold = threshold_percent
        self.enable_repair = enable_repair

    def validate(self, data):
        violations = []
        for i in range(1, len(data)):
            prev, curr = data[i-1]['price'], data[i]['price']
            change = abs(curr - prev) / prev
            if change > self.threshold:
                violations.append({
                    "type": "PRICE_SPIKE",
                    "timestamp": data[i]['timestamp'],
                    "detail": f"Jump of {change:.2%}"
                })
        return violations

    def repair(self, data):
        if not self.enable_repair:
            return data

        repaired = copy.deepcopy(data)

        for i in range(1, len(repaired)):
            prev, curr = repaired[i-1]['price'], repaired[i]['price']
            change = abs(curr - prev) / prev
            if change > self.threshold:
                repaired[i]['price'] = (prev + curr) / 2

        return repaired
    
import copy

class MonotonicTimeRule(ValidationRule):
    def __init__(self, enable_repair=False):
        self.enable_repair = enable_repair

    def validate(self, data):
        violations = []
        for i in range(1, len(data)):
            if data[i]['timestamp'] <= data[i-1]['timestamp']:
                violations.append({
                    "type": "TIME_ORDER_ERROR",
                    "timestamp": data[i]['timestamp'],
                    "detail": "Timestamp is not sequential"
                })
        return violations

    def repair(self, data):
        if not self.enable_repair:
            return data

        repaired = copy.deepcopy(data)

        for i in range(1, len(repaired)):
            if repaired[i]['timestamp'] <= repaired[i-1]['timestamp']:
                repaired[i]['timestamp'] = repaired[i-1]['timestamp'] + 1

        return repaired
    
class StatisticalOutlierRule(ValidationRule):
    def __init__(self, z_threshold=3):
        self.z_threshold = z_threshold

    def validate(self, data):
        prices = [d["price"] for d in data]
        mean = sum(prices) / len(prices)
        std = (sum((p - mean) ** 2 for p in prices) / len(prices)) ** 0.5

        violations = []
        for d in data:
            z = abs(d["price"] - mean) / std if std else 0
            if z > self.z_threshold:
                violations.append({
                    "type": "STATISTICAL_OUTLIER",
                    "timestamp": d["timestamp"],
                    "detail": f"Z-score {z:.2f}"
                })

        return violations