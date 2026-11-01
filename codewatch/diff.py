"""Parse git diff output into per-file changed lines."""

from __future__ import annotations
import os
import subprocess

def get_diff(ref: str = "HEAD~1") -> str:
    """Return unified diff of commits in `ref`, not the working tree.

    A range (`a..b` / `a...b`) is used as-is. A single ref becomes
    `ref...HEAD` so a pre-push hook can pass the remote SHA.
    """
    range_spec = ref if ".." in ref else f"{ref}...HEAD"
    try:
        result = subprocess.run(
            ["git", "diff", range_spec, "--unified=0"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        result = subprocess.run(
            ["git", "diff", "--cached", "--unified=0"],
            capture_output=True,
            text=True,
        )
        return result.stdout


def parse_diff(raw_diff: str) -> dict[str, list[str]]:
    """
    Parse a unified diff string into a mapping of filename → added lines.

    Returns only .py files. Skips binary files and deleted files.
    Uses the new filename for renamed files.
    """
    result: dict[str, list[str]] = {}
    current_file: str | None = None

    for line in raw_diff.splitlines():
        if line.startswith("+++ "):
            path = line[4:]
            if path.startswith("b/"):
                path = path[2:]
            if path.endswith(".py") and path != "/dev/null":
                current_file = path
                if current_file not in result:
                    result[current_file] = []
            else:
                current_file = None
            continue

        if line.startswith("+") and not line.startswith("+++") and current_file:
            result[current_file].append(line[1:])

    return result


def added_file_linenos(filename: str, added_lines: list[str]) -> list[int]:
    """Map each added line to its 1-based line number in `filename`.

    Falls back to 1, 2, 3... when the file is missing (unit tests).
    Duplicate lines consume the next unused match in file order.
    """
    if not added_lines:
        return []
    if not os.path.exists(filename):
        return list(range(1, len(added_lines) + 1))

    try:
        source = open(filename, encoding="utf-8").read().splitlines()
    except (OSError, UnicodeDecodeError):
        return list(range(1, len(added_lines) + 1))

    used: set[int] = set()
    linenos: list[int] = []
    for i, added in enumerate(added_lines, start=1):
        found = 0
        for n, src in enumerate(source, start=1):
            if n in used:
                continue
            if src == added:
                found = n
                used.add(n)
                break
        linenos.append(found or i)
    return linenos


def get_changed_files(ref: str = "HEAD~1") -> list[str]:
    """Return list of changed .py filenames (relative paths)."""
    try:
        result = subprocess.run(
            ["git", "diff", ref, "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [f for f in result.stdout.splitlines() if f.endswith(".py")]
    except subprocess.CalledProcessError:
        return []
