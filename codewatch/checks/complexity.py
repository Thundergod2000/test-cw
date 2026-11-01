"""Cyclomatic complexity check using radon."""

from __future__ import annotations
import os
from codewatch.diff import added_file_linenos
from codewatch.types import CheckResult, Violation, Severity

COMPLEXITY_THRESHOLD = 10  # warn above this, block above ERROR_THRESHOLD
ERROR_THRESHOLD = 20


def check_complexity(filename: str, added_lines: list[str]) -> CheckResult:
    """
    Measure cyclomatic complexity of functions in the changed file.

    Uses radon — reads the file from disk so it gets full function context,
    not just the diff lines (complexity can't be measured on snippets).
    """
    try:
        from radon.complexity import cc_visit
    except ImportError:
        return CheckResult(
            check_name="complexity",
            passed=True,
            skipped=True,
            skip_reason="radon not installed — run: pip install radon",
        )

    if not added_lines:
        return CheckResult(check_name="complexity", passed=True)

    if not os.path.exists(filename):
        return CheckResult(
            check_name="complexity",
            passed=True,
            skipped=True,
            skip_reason=f"{filename} not found on disk (deleted or renamed)",
        )

    try:
        source = open(filename).read()
    except (OSError, UnicodeDecodeError) as e:
        return CheckResult(
            check_name="complexity",
            passed=True,
            skipped=True,
            skip_reason=f"could not read file: {e}",
        )

    violations: list[Violation] = []

    try:
        blocks = cc_visit(source)
    except SyntaxError:
        return CheckResult(
            check_name="complexity",
            passed=True,
            skipped=True,
            skip_reason="syntax error in file — fix syntax before complexity check",
        )

    added_nums = set(added_file_linenos(filename, added_lines))

    for block in blocks:
        end = getattr(block, "endline", block.lineno)
        if added_nums and not any(n in added_nums for n in range(block.lineno, end + 1)):
            continue
        if block.complexity > ERROR_THRESHOLD:
            violations.append(Violation(
                line=block.lineno,
                message=(
                    f"{block.name}() has complexity {block.complexity} "
                    f"(limit {ERROR_THRESHOLD}) — break it into smaller functions"
                ),
                severity=Severity.ERROR,
            ))
        elif block.complexity > COMPLEXITY_THRESHOLD:
            violations.append(Violation(
                line=block.lineno,
                message=(
                    f"{block.name}() has complexity {block.complexity} "
                    f"(threshold {COMPLEXITY_THRESHOLD}) — consider simplifying"
                ),
                severity=Severity.WARNING,
            ))

    return CheckResult(
        check_name="complexity",
        passed=not any(v.severity == Severity.ERROR for v in violations),
        violations=violations,
    )
