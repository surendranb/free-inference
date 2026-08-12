# Contributing

Free-inference is a community-maintained catalog of free LLM inference options — for humans and agents.

## What makes a good PR

The catalog only ships what is **free today and verifiable**. Every model row carries a `verified` date; the nightly probe (`probe.py`) re-checks Google + OpenRouter automatically. For anything else, verification is manual.

**Preferred PRs, in order:**

1. **Fix an error** — wrong RPM/context/cost, dead model, broken URL. Best kind.
2. **Add a provider or model that is genuinely free** — no-card free tier, or a promo with a date. Include the source URL in the PR description.
3. **Improve the data schema / build / probe** — schema is `data/schema.json`, single source of truth is `data/providers.json`, generator is `build.py` (stdlib only, keep it that way).

## How to contribute

1. Fork the repo, edit `data/providers.json` (find the provider, adjust the model rows).
2. Set `"verified": "YYYY-MM-DD"` to today.
3. Run locally to confirm nothing breaks:
   ```
   python3 build.py
   ```
4. Open a PR. In the description: what changed, and the URL/evidence you verified against.

## What gets merged

- Corrections with evidence: merged fast.
- Additions with a source link: reviewed; if the claim is unverifiable, expected to be flagged.
- Anything that breaks the build: closed.

## What does NOT get merged

- Paid/hidden-paywall "free trials" without a clear cap.
- Models that were deprecated or shut down (the probe removes these automatically).
- Sensitive data, keys, or personal info — the repo is public and scanned.

The maintainer runs the nightly probe; keep your rows honestly dated and they'll stay honest.