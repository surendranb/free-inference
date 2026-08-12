# Free Inference

A living catalog of every provider that gives developers **free API access to LLM inference** — usable from a harness, agent, or CLI. Web-chat-only free tiers (ChatGPT, Claude.ai, Gemini app, deepseek.com, Grok, Copilot) are excluded on purpose.

Live site: **https://freeinference.dev** (interactive, two-pane UI with filtering and sorting per model column).

## What's inside

| File | What it is |
| --- | --- |
| `data/providers.json` | **Single source of truth** — one JSON file, all providers and models |
| `dist/index.html` | Generated site (two-pane catalog, no-JS fallback) |
| `dist/llms.txt` | Agent-readable summary (llmstxt.org) — point LLMs here |
| `dist/data/schema.json` | JSON Schema — validate `providers.json` before trusting it |
| `probe.py` | Nightly verifier: Google + OpenRouter rows are synced from their live APIs |
| `build.py` | Regenerates everything in `dist/` from `providers.json` |

## How to use the data

The machine-readable endpoint of the site is `https://freeinference.dev/data/providers.json` (validate against `.../data/schema.json`). There is no API key, no CORS restriction — fetch it from any agent or CLI.

Example (any language):

```
curl -s https://freeinference.dev/data/providers.json | jq '.providers[] | {name, free_type}'
```

## How it stays correct

- **Nightly probe** (GitHub Actions, 03:37 UTC): `probe.py` calls the Google and OpenRouter APIs and syncs those rows to what the endpoints actually report. No live endpoint → the 45-day staleness flag kicks in and the row is marked for human verification.
- **Every row cites a primary source** — the provider name links to official docs/limits pages.
- **PRs welcome.** Corrections and additions require a primary-source link + verification date; unverifiable rows get rejected (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Running it locally

```bash
# regenerate dist/ from data/providers.json
python3 build.py

# verify Google + OpenRouter rows against their live APIs
# (GEMINI_API_KEY from env or macOS Keychain; OpenRouter needs no key)
python3 probe.py
```

## Contributing

Edit `data/providers.json`, run `python3 build.py` to confirm the build passes, open a PR. Details in [CONTRIBUTING.md](CONTRIBUTING.md). MIT license — see [LICENSE](LICENSE).

## Caveats

Limits change without notice and vary per model, account age, region, and peak hours. Treat this table as a map, not a contract — verify before you architect on it.