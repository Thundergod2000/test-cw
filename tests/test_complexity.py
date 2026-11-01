"""Tests for complexity check — only newly added functions."""

from codewatch.checks.complexity import check_complexity


OLD = """
def old_nested(a, b, c, d, e, f, g):
    if a:
        if b:
            if c:
                for x in d:
                    if e:
                        if f == 1:
                            return x
                        elif f == 2:
                            return x * 2
                        elif f == 3:
                            return x * 3
                        elif f == 4:
                            return x * 6
                        else:
                            if g:
                                return x * 4
                            else:
                                return x * 5
    return None
"""

NEW = """
def ping():
    return 1
"""


def test_old_complex_function_ignored(tmp_path, monkeypatch):
    src = tmp_path / "mod.py"
    src.write_text(OLD + NEW, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    result = check_complexity("mod.py", ["def ping():", "    return 1"])
    assert result.violations == []


def test_new_complex_function_flagged(tmp_path, monkeypatch):
    src = tmp_path / "mod.py"
    src.write_text(OLD, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    added = OLD.strip().splitlines()
    result = check_complexity("mod.py", added)
    assert result.violations
    assert result.violations[0].line == 2
