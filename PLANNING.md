# CodeWatch — Build Plan

This is the single source of truth for what we are building, in what order,
and why. Read this before starting any feature.

---

## The one-line goal

Ship a working CLI tool that catches bad Python code before it gets pushed
to git, impressive enough to demo in a job interview for an AI/GenAI role.

---

## What is in scope RIGHT NOW

These are the only things being built. Nothing else.

### ✅ Already built
- [x] Project scaffold (folders, pyproject.toml, entry point)
- [x] git diff parser — reads changed files from git
- [x] 5 static checks: secrets, complexity, dead_code, tests, docstrings
- [x] Terminal reporter — coloured output, PASS/WARN/FAIL
- [x] pre-push hook installer (`codewatch install-hook`)
- [x] JSON output mode (`--format json`)
- [x] 10 passing tests

### 🔨 Building next (in this order)

**Step 1 — Make the demo impressive**
- Stress test file that triggers every check dramatically
- Clean demo script that shows before/after in 60 seconds
- README with a GIF or screenshot of it working

**Step 2 — Multi-account key rotation**
- Read a list of API keys from environment or .env
- Try key 1, if rate-limited or out of tokens → try key 2
- If all keys fail → fall back to static-only mode silently

**Step 3 — Token reduction (RTK)**
- Strip unchanged lines from diff before any API call
- Cache system prompt between calls
- Bundle all AI checks into one call, not many

**Step 4 — Package and distribute**
- Push to PyPI so anyone can `pip install codewatch-lite`
- Write a one-page landing page (can be GitHub README)
- Tag v0.1.0 release on GitHub

**Step 5 — Deploy (for the AI version)**
- Simple FastAPI server that accepts webhook from GitHub
- One endpoint: POST /review — takes a diff, returns verdict
- Deploy to Railway or Render (free tier, no credit card needed)

---

## What is OUT of scope (skip these for now)

| Feature | Why skipped |
|---|---|
| Web dashboard | Takes weeks, adds no demo value right now |
| Database / history | Not needed until there are paying users |
| Multi-language (JS, Java) | Python alone is enough for the demo |
| Config file support | Hard-coded defaults work fine for MVP |
| GitHub Actions integration | Webhook deploy covers this later |
| Architecture checks | Needs RAG + embeddings — Phase 2 |
| Scalability work | Premature — get users first |

---

## Phase map — big picture

```
Phase 1 (NOW)    → CodeWatch Lite CLI — working, installable, demo-ready
Phase 2 (Next)   → CodeWatch AI — adds Claude API layer on top of Lite
Phase 3 (Later)  → CodeWatch SaaS — web dashboard, teams, billing
```

We are in Phase 1. Do not build Phase 2 or 3 features right now.

---

## Demo flow (what the interviewer will see)

The demo should take under 2 minutes and show this sequence:

```
1. Developer adds bad code (hardcoded password, no docstring, complex function)
2. Developer tries to push: git push
3. codewatch fires automatically (pre-push hook)
4. Terminal shows FAIL with exact line numbers and explanations
5. Push is blocked
6. Developer fixes the password (moves to env var)
7. Developer pushes again
8. codewatch shows PASS
9. Push goes through
```

This is the entire demo. Keep it to this. Do not show config files,
dashboards, or anything else.

---

## Why this is good for an AI/GenAI job application

- Shows you understand how to wrap an AI API in a real product
- Shows you understand token costs and how to reduce them
- Shows you built something end-to-end, not just a notebook
- The multi-account key rotation shows practical LLM operations knowledge
- The static-first, AI-second architecture shows you think about cost

When asked in an interview: "What would you do differently?"
Answer: "I'd add RAG to give the AI context about the project's existing
architecture so it gives project-specific feedback, not generic feedback."
That answer shows depth.

---

## Decisions still open (things to choose before building)

### Decision 1: Where to store API keys for multi-account rotation?

**Option A: .env file** (simpler)
- Keys go in a .env file, loaded with python-dotenv
- Tradeoff: developer has to manage the file manually, easy to accidentally commit it

**Option B: Environment variables** (safer)
- Keys set in the shell: `export CLAUDE_KEY_1=sk-ant-...`
- Tradeoff: harder to set up for non-technical users, but safer

**Recommendation:** Start with .env, add a .gitignore entry for it.

### Decision 2: What to do when all API keys are exhausted?

**Option A: Fail open** — run static checks only, skip AI checks
- Tradeoff: developer gets partial feedback, doesn't know AI was skipped unless they read logs

**Option B: Fail with warning** — show a clear message that AI checks were skipped
- Tradeoff: slightly more friction but developer always knows what ran

**Recommendation:** Option B — transparency builds trust.

### Decision 3: Deploy target for the AI version

**Option A: Railway** — free tier, deploys from GitHub, zero config
- Tradeoff: free tier sleeps after inactivity (30s cold start for demo)

**Option B: Render** — similar to Railway, slightly more reliable free tier
- Tradeoff: same cold start problem

**Option C: Fly.io** — more control, stays awake on free tier
- Tradeoff: slightly more setup

**Recommendation:** Railway for speed. Upgrade to Fly.io if cold starts
become a demo problem.
