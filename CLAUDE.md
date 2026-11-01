# CodeWatch — AI Coding Guide

This file tells the AI (Cursor, Claude, etc.) everything it needs to know
about this project. Read this before writing any code.

---

## What this project is

CodeWatch is a code quality tool that catches bad code before it reaches
a git repo. It runs when a developer tries to push code and either blocks
the push or warns them about problems.

There are two versions:
- **CodeWatch Lite** — no AI, runs offline, checks Python code only
- **CodeWatch AI** — uses Claude API, smarter checks, costs tokens

Right now we are building **CodeWatch Lite** first. Get that working and
shipped. Everything else comes later.

---

## The goal of this build

1. Have a working demo good enough to show in a job interview
2. Put it on a resume as a real shipped product
3. Get it to a point where someone can install and use it

This is NOT about perfect code. It is about working code that does
something real and impressive.

---

## Tech stack

```
Language:     Python 3.9+
CLI tool:     argparse (built into Python, no extra install)
Checks use:   radon (complexity), vulture (dead code), stdlib ast
Tests:        pytest
Package:      pyproject.toml with pip install support
```

No web framework. No database. No frontend. Just a CLI tool for now.

---

## Folder structure

```
codewatch-lite/
├── codewatch/
│   ├── __init__.py
│   ├── cli.py          ← entry point, handles codewatch scan / install-hook
│   ├── scanner.py      ← runs all checks, decides pass/block
│   ├── reporter.py     ← prints results to terminal
│   ├── diff.py         ← parses git diff output
│   ├── types.py        ← shared data types (CheckResult, Violation)
│   └── checks/
│       ├── __init__.py
│       ├── secrets.py      ← finds hardcoded passwords/keys
│       ├── complexity.py   ← finds overly complex functions
│       ├── dead_code.py    ← finds unused functions/variables
│       ├── tests.py        ← checks if test file exists
│       └── docstrings.py   ← checks public functions have docstrings
├── tests/
│   ├── test_secrets.py
│   ├── test_diff.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## How each check works (simple version)

**secrets.py** — goes line by line through added code, runs regex patterns
looking for things like `password = "abc"` or `api_key = "sk-..."`. If it
finds one, it's an ERROR that blocks the push.

**complexity.py** — uses the `radon` library to count how many different
paths through a function exist. A simple function scores 1. A function
with 20 if/else branches scores 20+. Above 20 = block, above 10 = warn.

**dead_code.py** — uses the `vulture` library to find functions/variables
that are defined but never used anywhere. Always a warning, never blocks.

**tests.py** — checks if a file called `test_<filename>.py` exists in the
tests/ folder. If not, warns the developer. Never blocks.

**docstrings.py** — uses Python's AST (code parser) to find public
functions (not starting with _) that have no docstring. Always warns.

---

## Data types — always use these, never plain dicts

```python
# Every check returns a CheckResult
@dataclass
class Violation:
    line: int           # which line has the problem
    message: str        # what the problem is, in plain English
    severity: Severity  # ERROR (blocks) or WARNING (just warns)

@dataclass
class CheckResult:
    check_name: str             # e.g. "secrets"
    passed: bool                # False only if there are ERROR violations
    violations: list[Violation] # empty list if all good
    skipped: bool = False       # True if check couldn't run
    skip_reason: str = ""       # why it was skipped
```

---

## Rules for writing checks

1. Every check function signature must be:
   `def check_something(filename: str, added_lines: list[str]) -> CheckResult`

2. If a library is missing, return a skipped CheckResult — never crash

3. If the file doesn't exist on disk, return a skipped CheckResult

4. Secrets = ERROR (blocks push). Everything else = WARNING (allows push)

5. Only flag things in the added lines (new code), not old existing code

---

## Token saving (RTK — Reduce Token Cost)

When using Claude API (CodeWatch AI version, not Lite), follow these rules
to keep API costs low:

1. **Run static checks first, before calling Claude.** Things like secret
   detection and complexity scoring cost zero tokens. Only call Claude for
   things static analysis cannot judge.

2. **Strip the diff before sending it.** Remove unchanged context lines.
   Only send lines that actually changed (lines starting with + in the diff).

3. **Use prompt caching.** The system prompt and project rules stay the
   same across many pushes. Cache them so you only pay for the diff part.

4. **Never send the whole file.** Only send the changed lines plus the
   function signature they belong to (for context).

5. **One API call per push, not one per check.** Bundle all the things
   that need Claude into a single prompt with a JSON response.

---

## Multi-account API key rotation

When one Claude API account runs out of tokens, automatically switch to
the next account. Store keys in a list, track which one is active.

```python
# In config or .env file
CLAUDE_API_KEYS = [
    "sk-ant-key1...",
    "sk-ant-key2...",
    "sk-ant-key3...",
]
```

The key manager tries the first key. If it gets a 429 (rate limit) or
402 (payment required), it moves to the next key. Never crashes — if all
keys are exhausted, falls back to static-only mode (no Claude, just the
5 checks).

---

## How to run the project locally

See TESTING.md for the full local test setup.

Quick version:
```bash
pip install -e ".[dev]"    # install in dev mode
pytest tests/              # run all tests
codewatch --help           # verify CLI works
```

---

## What NOT to build right now

Skip these — they are post-MVP:
- Web dashboard or UI
- Database or history tracking  
- Multi-language support (JS, Java, etc.)
- Config file (.codewatch.yml) support
- CI/CD GitHub Actions integration
- SARIF output format
- Architecture constraint checking
- Scalability or performance optimisation
- Proper logging system
- Authentication or user accounts

If you are about to build any of these, stop and check with the developer.

---

## Writing style for code

- Simple variable names. `lines` not `source_line_collection`
- Short functions. If a function is over 30 lines, split it
- One job per function. A function that parses AND validates is two functions
- Comments explain WHY, not WHAT. The code shows what. Comments show why
- No clever one-liners that need a minute to understand
