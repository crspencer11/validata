from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Violation:
    type: str
    timestamp: int
    detail: str

@dataclass
class ValidationResult:
    status: str
    violation_count: int
    violations: List[Violation]
    repaired_data: Optional[list[dict]] = None