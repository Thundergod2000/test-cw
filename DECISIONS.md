# CodeWatch — Decisions Log

Every important choice that was made, why it was made, and what the
tradeoff was. When in doubt about why something is the way it is,
look here first.

---

## D1 — Python only for v1

**Decision:** Only scan Python files. Ignore JS, Java, TypeScript etc.

**Why:** Building one language deeply is better than three languages
poorly. Python has the best AST tooling (`ast` module is in stdlib).
The demo audience is Python developers.

**Tradeoff:** Limits the market. A JS-heavy team cannot use this.
Acceptable for now — ship first, expand later.

**Still locked:** Yes

---

## D2 — 5 checks only

**Decision:** Only these 5 checks in v1:
1. Secret detection
2. Cyclomatic complexity
3. Dead code
4. Test presence
5. Docstring presence

**Why:** Each one is fast, deterministic, and has zero false positives
on clear cases. Each one catches something a senior engineer would
actually care about.

**Tradeoff:** Misses many real issues (circular imports, SQL injection,
type errors, performance problems). Acceptable — these 5 make a strong
demo and real catches.

**Still locked:** Yes

---

## D3 — Secrets always block; complexity blocks only when extreme

**Decision:** A push is blocked (exit code 1) when:
1. Secret detection finds a hardcoded password/key, or
2. Cyclomatic complexity of a changed function is above 20

Complexity between 11 and 20 warns. Dead code, missing tests, and
missing docstrings always warn and never block.

**Why:** Hardcoded secrets are always wrong. A function with complexity
over 20 is also a hard fail — it is untestable in practice. Softer
quality issues (docs, tests, unused code) should not brick a push, or
developers will disable the hook.

This matches the README and the current implementation.

**Tradeoff:** Complexity false positives can still block a push. The
threshold is high (20) to keep that rare. Rahul (validation interview)
said the tool needs monitoring in the initial phase — warnings cover
that; only the two cases above are hard blocks.

**Still locked:** Yes

---

## D4 — No LLM in CodeWatch Lite

**Decision:** CodeWatch Lite uses zero AI. Pure Python static analysis.

**Why:** This is actually a feature, not a compromise:
- Works offline (no internet needed)
- Zero token cost
- Deterministic (same code = same result every time)
- Faster (no API call latency)

Developers who are sceptical of AI tools will trust this more.

**Tradeoff:** Cannot make judgement calls about code quality ("is this
abstraction the right one?"). That requires CodeWatch AI (Phase 2).

**Still locked:** Yes

---

## D5 — Diff-scoped scanning only

**Decision:** Only scan files that changed in the current push, not
the entire codebase.

**Why:** Full-project scans on a large repo take too long for a
pre-push hook. A pre-push hook that takes 30 seconds will be disabled
by developers within a week.

**Tradeoff:** Misses pre-existing problems in files you didn't touch.
Acceptable — you can always run a full scan separately. The hook only
covers what changed.

**Still locked:** Yes

---

## D6 — No dashboard, no database in v1

**Decision:** No web UI. No storing results. Terminal output only.

**Why:** A dashboard adds 2-3 weeks of work and zero additional
demo value. The terminal output is the product for now.

**Tradeoff:** No history, no trends, no team view. All of that is
Phase 3. Acceptable.

**Still locked:** Yes

---

## D7 — Charge from day one

**Decision:** No free-forever tier. Charge for the product.

**Why:** Free users give feedback. Paying users give real signal.
A paying customer tells you what is actually worth fixing.

**Tradeoff:** Harder to get initial users. Offset by doing validation
interviews first (like the Rahul interview) to know people want it
before building.

**Billing options:** Stripe (more control) or Gumroad (zero setup).
Gumroad recommended for v1 — it takes 10 minutes to set up.

**Still locked:** Yes

---

## D8 — Token reduction strategy (RTK)

**Decision:** When AI mode is used, reduce tokens with these steps
in order:

1. Run all 5 static checks first. Only call Claude for what they miss.
2. Strip unchanged lines from diff before sending to Claude.
3. Use prompt caching for the system prompt (same every call).
4. One Claude call per push, not one per check.

**Why:** A naive implementation sends 15-20K tokens per push.
These steps bring it to 2-4K per push — roughly 80% cost reduction.
This is what makes the SaaS version economically viable.

**Tradeoff:** More complex code in the API client layer. Worth it
because token cost is the main operational expense at scale.

**Status:** Design decided. Not built yet.

---

## D9 — Multi-account key rotation

**Decision:** Accept a list of API keys. Try them in order. Switch
to next key on rate limit or payment error. Fall back to static-only
if all keys are exhausted.

**Why:** Allows running the demo or development work across multiple
free-tier accounts without interruption.

**Tradeoff:** Against Anthropic's terms of service if used to bypass
rate limits in production. Fine for personal development and demos.
Do not advertise this as a feature to customers.

**Status:** Design decided. Not built yet.

---

## D10 — Deploy target

**Decision:** Railway for the AI version webhook server.

**Why:** Deploys from GitHub in under 5 minutes. Free tier available.
No credit card needed. Good enough for a demo.

**Tradeoff:** Free tier sleeps after 15 minutes of inactivity.
First request after sleep takes 20-30 seconds (cold start).
For a live demo, send one warm-up request before the audience arrives.

**Status:** Not deployed yet.
