import logging

class DataValidator:
    def __init__(self, rules=None, repair_mode=False):
        self.rules = rules or []
        self.repair_mode = repair_mode
        self.logger = logging.getLogger(__name__)

    def run(self, data: list[dict]):
        all_violations = []
        for rule in self.rules:
            self.logger.info(f"Running {rule.__class__.__name__}...")
            violations = rule.validate(data)
            all_violations.extend(violations)
        
        if self.repair_mode:
            self.logger.info("Repair mode is enabled. Attempting to repair data...")
            data = self.repair_data(data, all_violations)

        return {
            "status": "FAILED" if all_violations else "PASSED",
            "count": len(all_violations),
            "violations": all_violations,
            "repaired_data": data if self.repair_mode else None
        }

    def repair_data(self, data: list[dict], violations: list[dict]):
        # Implement repair logic based on the violations
        for violation in violations:
            if violation['type'] == "PRICE_SPIKE":
                # Example repair logic: interpolate or adjust prices
                self.logger.info(f"Repairing price spike at {violation['timestamp']}")
                # Actual repair logic would go here
        return data  # Return the repaired data