# CodeWatch — Deployment Guide

How to get CodeWatch running somewhere people can access it.
This covers two things: the CLI tool (no server needed) and the
AI version (needs a server).

---

## Part 1 — CLI tool (CodeWatch Lite)

The CLI tool does not need a server. Users install it directly on
their own machine. This is covered in DISTRIBUTION.md.

---

## Part 2 — AI version server (CodeWatch AI)

The AI version needs a small server that:
- Receives a git diff from a developer's machine
- Runs the 5 static checks
- Calls Claude API for deeper analysis
- Returns the verdict (pass / warn / block + reasons)

This is a simple REST API with one endpoint.

---

## Recommended: Deploy to Railway

Railway is the fastest way to get a server running. Takes about
10 minutes. Free tier available.

### Step 1 — Prepare your code

Your server needs one file added: `server.py`

```python
"""Simple FastAPI server for CodeWatch AI mode."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="CodeWatch AI")

class ReviewRequest(BaseModel):
    diff: str
    project_name: str = "unknown"

@app.get("/health")
def health():
    """Railway uses this to check if the server is running."""
    return {"status": "ok"}

@app.post("/review")
def review(request: ReviewRequest):
    """
    Accept a git diff, run checks, return verdict.
    Called by the codewatch CLI when AI mode is enabled.
    """
    from codewatch.diff import parse_diff
    from codewatch.scanner import run_checks, should_block
    from codewatch.reporter import _build_json_output  # we'll add this

    changed_files = parse_diff(request.diff)
    if not changed_files:
        return {"verdict": "pass", "message": "no Python files changed"}

    results = run_checks(changed_files)
    blocked = should_block(results)

    return {
        "verdict": "block" if blocked else "pass",
        "results": results  # TODO: serialise CheckResult properly
    }
```

Also add `requirements.txt`:
```
fastapi
uvicorn
radon
vulture
anthropic
python-dotenv
```

### Step 2 — Push to GitHub

```bash
git init  # if not already a git repo
git add .
git commit -m "ready for deployment"
# Create a repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/codewatch-lite.git
git push -u origin main
```

### Step 3 — Deploy on Railway

1. Go to railway.app — sign up with GitHub (free)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your codewatch-lite repo
4. Railway detects Python automatically
5. Add environment variables:
   - Click "Variables" tab
   - Add `CLAUDE_API_KEY` = your Anthropic key
   - Add `PORT` = 8000
6. Add a start command:
   - Click "Settings" → "Start Command"
   - Enter: `uvicorn server:app --host 0.0.0.0 --port $PORT`
7. Click "Deploy"

Railway gives you a URL like `https://codewatch-production.up.railway.app`

### Step 4 — Test the deployment

```bash
# Health check
curl https://your-app.up.railway.app/health

# Should return: {"status": "ok"}
```

### Step 5 — Connect CLI to the server

Add a `--remote` flag to the CLI that sends the diff to your server
instead of running checks locally.

```bash
codewatch scan --diff HEAD~1 --remote https://your-app.up.railway.app
```

---

## Alternative: Render

If Railway's free tier is not available, use Render.

1. Go to render.com → sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (same as Railway)
7. Click "Create Web Service"

Same result, slightly different UI.

---

## Keeping the server awake for demos

Free tier servers on Railway and Render sleep after 15 minutes
with no traffic. When they sleep, the first request takes 20-30
seconds. That will ruin a live demo.

**Fix:** Send a warm-up request before the demo starts.

```bash
# Run this 1 minute before your demo
curl https://your-app.up.railway.app/health
```

This wakes the server up so it is ready when you need it.

---

## Environment variables reference

| Variable | What it does | Required |
|---|---|---|
| `CLAUDE_API_KEY` | Primary Anthropic API key | Yes (AI mode) |
| `CLAUDE_API_KEY_2` | Backup key (key rotation) | No |
| `CLAUDE_API_KEY_3` | Third backup key | No |
| `PORT` | Which port the server listens on | Yes (Railway sets it) |
| `BLOCK_ON_SECRETS` | Set to "false" to warn-only | No |

---

## Checking if deployment worked

After deploying, run through this checklist:

```
[ ] curl /health returns {"status": "ok"}
[ ] Sending a diff with a hardcoded password returns "block"
[ ] Sending clean code returns "pass"
[ ] Server logs are visible in Railway/Render dashboard
[ ] Cold start after 20 minutes takes under 35 seconds
```

If all pass, deployment is done.
