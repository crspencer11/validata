from abc import ABC, abstractmethod

class ValidationRule(ABC):
    @abstractmethod
    def validate(self, data: list[dict]) -> list[dict]:
        """Returns a list of violation records."""
        pass

class PriceSpikeRule(ValidationRule):
    def __init__(self, threshold_percent=0.10):
        self.threshold = threshold_percent

    def validate(self, data: list[dict]) -> list[dict]:
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

class MonotonicTimeRule(ValidationRule):
    def validate(self, data: list[dict]) -> list[dict]:
        violations = []
        for i in range(1, len(data)):
            if data[i]['timestamp'] <= data[i-1]['timestamp']:
                violations.append({
                    "type": "TIME_ORDER_ERROR",
                    "timestamp": data[i]['timestamp'],
                    "detail": "Timestamp is not sequential"
                })
        return violations

class RepairablePriceSpikeRule(PriceSpikeRule):
    def repair(self, data: list[dict]) -> list[dict]:
        repaired_data = data.copy()
        for i in range(1, len(repaired_data)):
            prev, curr = repaired_data[i-1]['price'], repaired_data[i]['price']
            change = abs(curr - prev) / prev
            if change > self.threshold:
                # Suggest a repair by averaging with the previous price
                repaired_data[i]['price'] = (prev + curr) / 2
        return repaired_data

class RepairableMonotonicTimeRule(MonotonicTimeRule):
    def repair(self, data: list[dict]) -> list[dict]:
        repaired_data = data.copy()
        for i in range(1, len(repaired_data)):
            if repaired_data[i]['timestamp'] <= repaired_data[i-1]['timestamp']:
                # Suggest a repair by incrementing the timestamp
                repaired_data[i]['timestamp'] = repaired_data[i-1]['timestamp'] + 1
        return repaired_data