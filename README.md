# CodeWatch Lite

Offline code governance for Python — catches quality issues before they reach your repo. No LLM, no network, no noise.

## What it checks

| Check | Blocks push | What it catches |
|---|---|---|
| Secrets | ✅ Yes | Hardcoded passwords, API keys, AWS credentials |
| Complexity | ✅ Yes (>20) / ⚠ Warn (>10) | Functions that are too complex to maintain |
| Dead code | ⚠ Warn | Unused functions, classes, variables |
| Test presence | ⚠ Warn | Source files with no matching test file |
| Docstrings | ⚠ Warn | Public functions and classes without docstrings |

## Install

```bash
pip install codewatch-lite
```

## Usage

```bash
# Scan your latest commit
codewatch scan

# Scan against a specific ref
codewatch scan --diff main

# Install as a pre-push hook (runs automatically on every push)
codewatch install-hook

# Get JSON output (for CI integration)
codewatch scan --format json
```

## Example output

```
FAIL  codewatch/app.py
       ✗  secrets
              ERROR   line 12: Password assignment detected — move to environment variable
       ✓  complexity
       ⚠  docstrings
              warn    line 8: Public function 'connect' has no docstring

✗  1 error(s), 2 total violation(s) across 1 file(s) — push blocked
```

## Configuration

Add a `.codewatch.yml` to your repo root to customise thresholds:

```yaml
# .codewatch.yml
complexity:
  warn_above: 10
  block_above: 20

checks:
  skip:
    - dead_code      # disable a check entirely
```

_(config file support coming in v0.2)_

## Requirements

- Python 3.9+
- Git
- `radon` and `vulture` (installed automatically)
