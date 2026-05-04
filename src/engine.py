import logging
from typing import List
from .models import ValidationResult, Violation

class DataValidator:
    def __init__(self, rules=None, repair_mode=False):
        self.rules = rules or []
        self.repair_mode = repair_mode
        self.logger = logging.getLogger(__name__)

    def run(self, data: List[dict]) -> ValidationResult:
        all_violations: List[Violation] = []

        for rule in self.rules:
            self.logger.info(f"Running {rule.__class__.__name__}...")
            violations = rule.validate(data)
            all_violations.extend([
                Violation(**v) for v in violations
            ])

        repaired_data = None

        if self.repair_mode:
            self.logger.info("Repair mode enabled")
            repaired_data = self.apply_repairs(data)

        return ValidationResult(
            status="FAILED" if all_violations else "PASSED",
            violation_count=len(all_violations),
            violations=all_violations,
            repaired_data=repaired_data
        )

    def apply_repairs(self, data: List[dict]) -> List[dict]:
        repaired = data.copy()

        for rule in self.rules:
            if hasattr(rule, "repair"):
                self.logger.info(f"Applying repair from {rule.__class__.__name__}")
                repaired = rule.repair(repaired)

        return repaired