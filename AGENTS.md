# FreeInference.dev — Agent Operating Rules

## Core Directive: Real-World Ground Truth Verification

1. **Antigravity Managed Agent as Maintainer**:
   Catalog verification and doc-auditing must be performed by the Antigravity Managed Agent (`antigravity-preview-09-2026` via the Google AI Studio Interactions API) running inside Google's hosted Linux sandbox with real Chrome and web access.
   
2. **Never Degrade to Synthetic Scrapers**:
   Do not use raw static HTML fetches (`urllib`, `requests`, `curl`) or regex string matching to verify provider offerings. Modern developer platforms and model aggregators use client-side hydration (SPAs), Cloudflare WAFs, and dynamic pricing tabs. Verification requires a real browser/agent runtime.

3. **Ground Truth Over Assumptions**:
   Never catalog a model or provider based on parametric memory or unverified claims. Every catalog entry must trace to an empirical verification event (live API probe or Antigravity browser agent audit).

4. **Surface Completeness**:
   Every programmatic `/free-*/` page must be maintained with $\ge 1$ verified model. Never break or drop programmatic routes.

5. **Deployment Invariants**:
   - Work in dedicated Git feature branches; never commit directly to `main`.
   - Rebuild `dist/` with `build.py` and verify all slices with `verify_matrix.py` before opening a PR.
