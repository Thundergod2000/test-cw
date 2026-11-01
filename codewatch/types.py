"""Shared data types for all checks."""

from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"    # blocks push
    WARNING = "warn"   # warns but allows


@dataclass
class Violation:
    line: int
    message: str
    severity: Severity = Severity.WARNING


@dataclass
class CheckResult:
    check_name: str
    passed: bool
    violations: list[Violation] = field(default_factory=list)
    skipped: bool = False
    skip_reason: str = ""
