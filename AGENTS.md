# FreeInference.dev — Agent Operating Rules

## Core Directive: Real-World Ground Truth Verification

1. **Three-Route Verification Priority**:
   - **Route 1 (Open Feeds)**: Prefer provider-published structured JSON/RSS feeds (`/api/v1/models`, `/api/gateway/models`, `/call/free_quota_config`, `/rest/v1/models_v2`).
   - **Route 2 (APIs & Machine Docs)**: Use live REST `/models` APIs and agent-native Markdown endpoints (`/llms.txt`, `/llms-full.txt`, `*.md` mirrors, `Accept: text/markdown`) navigated and reasoned over dynamically (`gemini-3.5-flash-lite`).
   - **Route 3 (Antigravity Managed Agent)**: Whenever a provider lacks valid machine-readable feeds/Markdown docs—or those docs are `inconclusive`—verification must escalate to `antigravity-preview-09-2026` driving real Chrome via the Interactions API.

2. **Never Degrade to HTML Scrapers**:
   Do not scrape raw HTML websites (`urllib`, `requests`, `curl`) or parse HTML tags with regex to verify `web` provider offerings. Only accept genuine machine-readable JSON/Markdown/RSS feeds or real Chrome execution via Antigravity.

3. **Ground Truth Over Assumptions**:
   Never catalog a model or provider based on parametric memory or unverified claims. Every catalog entry must trace to an empirical verification event (live feed/API probe, official `.md`/`llms.txt` doc verification, or Antigravity browser agent audit).

4. **Surface Completeness**:
   Every programmatic `/free-*/` page must be maintained with $\ge 1$ verified model. Never break or drop programmatic routes.

5. **Deployment Invariants**:
   - Work in dedicated Git feature branches; never commit directly to `main`.
   - Rebuild `dist/` with `build.py` and verify all slices with `verify_matrix.py` before opening a PR.
