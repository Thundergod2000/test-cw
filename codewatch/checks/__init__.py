"""All checks — import from here."""

from codewatch.checks.complexity import check_complexity
from codewatch.checks.dead_code import check_dead_code
from codewatch.checks.secrets import check_secrets
from codewatch.checks.tests import check_test_presence
from codewatch.checks.docstrings import check_docstrings

__all__ = [
    "check_complexity",
    "check_dead_code",
    "check_secrets",
    "check_test_presence",
    "check_docstrings",
]
