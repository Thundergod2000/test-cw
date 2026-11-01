"""Orchestrates all checks across changed files."""

from __future__ import annotations
from codewatch.types import CheckResult, Severity
from codewatch.checks import (
    check_complexity,
    check_dead_code,
    check_secrets,
    check_test_presence,
    check_docstrings,
)


def run_checks(changed_files: dict[str, list[str]]) -> dict[str, list[CheckResult]]:
    """
    Run all checks on each changed file.

    Args:
        changed_files: mapping of filename → list of added lines (from diff parser)

    Returns:
        mapping of filename → list of CheckResult (one per check)
    """
    results: dict[str, list[CheckResult]] = {}

    for filename, added_lines in changed_files.items():
        file_results = [
            check_secrets(filename, added_lines),
            check_complexity(filename, added_lines),
            check_dead_code(filename, added_lines),
            check_test_presence(filename, added_lines),
            check_docstrings(filename, added_lines),
        ]
        results[filename] = file_results

    return results


def should_block(results: dict[str, list[CheckResult]]) -> bool:
    """Return True if any check produced an ERROR-level violation."""
    for file_results in results.values():
        for result in file_results:
            for violation in result.violations:
                if violation.severity == Severity.ERROR:
                    return True
    return False
