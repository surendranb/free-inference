# Design: free-llm-providers release — repo + catalog website

Date: 2026-08-12 · Linear: [SUR-266](https://linear.app/surendran/issue/SUR-266) · Status: approved

## Outcome

Reliable, easily skimmable, updated information about every provider that gives
developers free API access to LLM inference — without bloat. Readable the same
way by humans (website, README) and agents (JSON, llms.txt, schema). The only
thing that matters: the number on the screen is true and current.

## 1. Data model — per-model records

`data/providers.json` restructures from provider-level blob strings to
per-model records. Providers keep identity columns; each gains `models[]`.

```json
{
  "name": "Z.AI (Zhipu)",
  "url": "https://docs.z.ai/guides/overview/rate-limits",
  "free_type": "Rate-limited free",
  "notes": "Free-tier limits revised twice in the past year - verify. Flash models free regardless of tier.",
  "verified": "2026-08-12",
  "models": [
    {
      "name": "GLM-4.7-Flash",
      "context": "203K",
      "rpm": "3",
      "tpm": "Not published",
      "rpd": "1000",
      "tpd": "Not published",
      "cost": "$0",
      "verified": "2026-08-12"
    }
  ]
}
```

Decision columns per model: context, RPM, TPM, RPD, day tokens, cost,
last-verified. Provider-level fields remain where a limit is provider-wide
(e.g. Hugging Face). Values stay display strings — limits change monthly and
numeric typing adds no decision power.

One-time data entry for ~50 models, transcribed from the existing table rows
plus the per-model detail already embedded in them ("Flash 10-15, Pro 5").

## 2. Auto-probe nightly — GitHub Action cron

`probe.py` — stdlib only (urllib, json):

- **Liveness**: HEAD/GET each provider's docs URL and base URL where known.
  Dead rows get flagged (`"dead": true`), never deleted.
- **Model presence**: fetch each provider's model list where an
  unauthenticated endpoint exists (Z.AI, OpenRouter, Groq, Cerebras, Google).
  Missing models flagged, existing numbers untouched.
- **Never edits numbers.** A probe confirms liveness; human-verified limits
  keep their date. "Verified" stamps auto-refresh only for probe-confirmed
  liveness of the provider, not limit accuracy.
- Runs daily ~05:00 UTC via GitHub Action (schedule + workflow_dispatch);
  `python3 probe.py --dry-run` works locally.
- On flagged changes: commits results, rebuilds site. Numbers change only via
  a human PR with a primary source cited (existing rule, unchanged).

## 3. Static + vanilla JS catalog

`build.py` keeps producing `index.html` — but as a two-pane catalog:

- **Left sidebar**: provider list — name, free-type chip
  (Rate-limited free / Promo free / Free gateway / Trial credits), free-model
  count, red dot if flagged dead. Search filter box on top.
- **Right panel**: selected provider's models table with decision columns
  (name, context, RPM, TPM, RPD, day tokens, cost, verified). Provider URL,
  notes, and free-type header above.
- **Vanilla JS** (~80-100 lines, no deps): render from embedded JSON,
  sidebar click, subject filter, sortable columns. No JS framework, no
  package.json, no build step beyond build.py.
- Palette stays Happy Hues #17 (cream/navy/pink/teal); no dark mode.
- Progressive: if JS is off, the page still renders the full table (current
  behavior preserved as fallback).

## 4. Agent consumption — one source, three doors

- **Repo**: `data/providers.json` (canonical, with schema).
- **Website**: `/data/providers.json` served byte-identical;
  `/llms.txt` (llmstxt.org standard: summary + one line per model);
  `/robots.txt` allowing all crawlers.
- **JSON Schema**: `data/schema.json` co-located with the data file —
  agents validate before trusting.

## 5. Repo release

- `git init`, GitHub public repo (name `free-llm-providers`), MIT license,
  `.gitignore` (nothing generated except via build.py), CONTRIBUTING section
  already in README.
- README keeps current single-table (human mirror) + adds per-model section
  and probe status.
- Cloudflare Pages: build command `python3 build.py`, output dir `.`, custom
  domain `freeinference.dev`. GitHub Action cron pushes probe commits, Pages
  rebuilds automatically.

## 6. Verification

1. `python3 probe.py --dry-run` — liveness logic runs without mutating data
2. `python3 build.py` — repo regenerates clean
3. `assert` self-check in build.py: every model has the required keys
4. Deploy to Pages preview; curl `/data/providers.json` on prod and diff
   byte-identical vs repo
5. Confirm llms.txt + robots.txt + schema.json reachable

## Out of scope

Frameworks, DB, analytics, rate-limit dashboards, accounts, paid tiers
catalog. Add only when someone asks.