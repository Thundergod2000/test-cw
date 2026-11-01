"""Run a before/after CodeWatch demo in a throwaway git repo."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent
SCAN = [sys.executable, "-m", "codewatch.cli", "scan", "--diff", "HEAD~1"]


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True)


def scan(repo: Path) -> int:
    result = subprocess.run(SCAN, cwd=repo)
    return result.returncode


def banner(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="codewatch-demo-") as raw:
        repo = Path(raw)
        git(repo, "init", "-b", "main")
        git(repo, "config", "user.email", "demo@example.com")
        git(repo, "config", "user.name", "CodeWatch Demo")

        (repo / "README.md").write_text("# demo\n", encoding="utf-8")
        git(repo, "add", "README.md")
        git(repo, "commit", "-m", "initial")

        banner("BEFORE — nightmare_code.py (expect FAIL, push blocked)")
        shutil.copy(DEMO_DIR / "nightmare_code.py", repo / "nightmare_code.py")
        git(repo, "add", "nightmare_code.py")
        git(repo, "commit", "-m", "add bad code")
        bad_code = scan(repo)

        banner("AFTER — clean_code.py (expect WARN or PASS, push allowed)")
        shutil.copy(DEMO_DIR / "clean_code.py", repo / "clean_code.py")
        git(repo, "add", "clean_code.py")
        git(repo, "commit", "-m", "add clean code")
        good_code = scan(repo)

        banner("Summary")
        print(f"nightmare_code.py exit code: {bad_code}  (want 1)")
        print(f"clean_code.py exit code:     {good_code}  (want 0)")
        print("\nOpen demo/nightmare_code.py and demo/clean_code.py to show the source.")
        return 0 if bad_code == 1 and good_code == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
