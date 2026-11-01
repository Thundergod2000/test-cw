# CodeWatch — Distribution Guide

How to get CodeWatch into developers' hands.
Two channels: PyPI (pip install) and GitHub releases (direct download).

---

## Channel 1 — PyPI (pip install codewatch-lite)

PyPI is the official Python package index. Publishing here means any
developer in the world can install your tool with one command:

```bash
pip install codewatch-lite
```

### Step 1 — Create a PyPI account

1. Go to pypi.org → "Register"
2. Verify your email
3. Go to "Account Settings" → "API tokens" → "Add API token"
4. Name it "codewatch-publish", scope: "Entire account"
5. Save the token — you only see it once

### Step 2 — Install publish tools

```bash
pip install build twine
```

**build** — creates the package files
**twine** — uploads them to PyPI

### Step 3 — Check your pyproject.toml is complete

Make sure these fields are filled in:

```toml
[project]
name = "codewatch-lite"          # must be unique on PyPI
version = "0.1.0"                 # update this for each release
description = "Offline code governance for Python"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
authors = [
    { name = "Madhu Dora", email = "madhudhora123@gmail.com" }
]
keywords = ["code-quality", "git", "static-analysis", "linting"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
```

### Step 4 — Build the package

```bash
# From inside the codewatch-lite folder
python -m build
```

This creates a `dist/` folder with two files:
- `codewatch_lite-0.1.0.tar.gz` (source distribution)
- `codewatch_lite-0.1.0-py3-none-any.whl` (wheel — faster to install)

### Step 5 — Test on TestPyPI first (recommended)

TestPyPI is a safe playground. Mistakes here do not affect the real PyPI.

```bash
# Upload to test environment
twine upload --repository testpypi dist/*

# Test install from test environment
pip install --index-url https://test.pypi.org/simple/ codewatch-lite
codewatch --help
```

If that works, go to the real PyPI.

### Step 6 — Upload to PyPI

```bash
twine upload dist/*
# Enter your PyPI username: __token__
# Enter your password: paste the API token from Step 1
```

Done. Anyone can now `pip install codewatch-lite`.

### Step 7 — Test the real install

```bash
# Uninstall your dev version first
pip uninstall codewatch-lite

# Install from PyPI
pip install codewatch-lite

# Should work
codewatch --help
```

---

## Releasing a new version

When you fix bugs or add features:

1. Update version in `pyproject.toml`: `version = "0.1.1"`
2. Update version in `codewatch/__init__.py`: `__version__ = "0.1.1"`
3. Build: `python -m build`
4. Upload: `twine upload dist/*`

PyPI keeps all old versions. Users get the new one on fresh install.

---

## Channel 2 — GitHub Releases (direct download)

Some developers prefer to download directly from GitHub rather than
using pip. GitHub Releases makes this easy.

### How to create a release

1. Go to your GitHub repo
2. Click "Releases" in the right sidebar → "Create a new release"
3. Tag version: `v0.1.0`
4. Title: `CodeWatch Lite v0.1.0`
5. Description: paste the key features and what was fixed
6. Attach files: drag the `.whl` and `.tar.gz` from your `dist/` folder
7. Click "Publish release"

Developers can then download and install:

```bash
pip install codewatch_lite-0.1.0-py3-none-any.whl
```

---

## Telling people about it

After publishing, share in these places:

**LinkedIn post (build-in-public):**
```
Just shipped CodeWatch Lite v0.1.0 — a CLI tool that catches 
hardcoded secrets, complex functions, and missing tests before 
they reach your git repo.

pip install codewatch-lite

Built it to solve a real problem: AI-generated code is fast but 
often skips docstrings and leaves debugging secrets in. This 
catches that automatically.

[link to GitHub repo]
```

**Show HN post (Hacker News):**
```
Show HN: CodeWatch Lite – offline Python code governance for pre-push hooks
```
Short description, link to GitHub, mention it works offline with zero API cost.

---

## Version numbering guide

Follow this pattern:

| Change type | Example | Version bump |
|---|---|---|
| Bug fix | Fixed false positive in secrets check | 0.1.0 → 0.1.1 |
| New check added | Added import order check | 0.1.1 → 0.2.0 |
| Breaking change | Renamed CLI flags | 0.2.0 → 1.0.0 |

Stay on 0.x.x until there are real users depending on it.
