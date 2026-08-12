# free-inference

Source repo for [freeinference.dev](https://freeinference.dev) — a catalog of providers that give developers free API access to LLM inference. The website is the product; this repo is where it's maintained.

## Repository layout

```
data/providers.json   # the catalog — single source of truth (edit this)
probe.py              # nightly verifier: re-checks live endpoints, syncs Google/OpenRouter rows
build.py              # generates dist/ (the website) from providers.json
dist/                 # build output — deployed to Cloudflare Pages, never committed
.github/workflows/    # nightly probe schedule
```

## How it works

1. All catalog data lives in `data/providers.json` — one file, everything else derives from it.
2. `build.py` turns it into the static site (`dist/`).
3. `probe.py` runs nightly (GitHub Actions): it calls the Google and OpenRouter APIs and rewrites those rows to match what the endpoints actually report, so the catalog can't go stale on its own.
4. Pushes to `main` publish a new build of the site.

## Local development

```bash
python3 build.py          # regenerate dist/ from data/providers.json
python3 probe.py          # verify live rows (Google needs GEMINI_API_KEY: env or macOS Keychain; OpenRouter is keyless)
```

## Contributing

Edit `data/providers.json`, run `python3 build.py` to confirm the build passes, open a PR. Every change must cite a primary source (official docs or dashboard) and a verification date — unverifiable rows are rejected. Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).