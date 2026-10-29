#!/usr/bin/env python3
"""Build Free Inference site artifacts from data/providers.json (single source of truth).

Outputs into dist/ (gitignored; deployed by Cloudflare Pages on push):
  dist/index.html           — two-pane catalog (sidebar providers | models panel), no-JS fallback
  dist/llms.txt             — agent-readable summary (llmstxt.org)
  dist/data/providers.json  — machine data
  dist/data/schema.json     — JSON Schema for providers.json (agents validate before trusting)
  dist/robots.txt           — allow all crawlers
"""
import hashlib
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data" / "providers.json").read_text())

COLS = DATA["columns"]
ROWS = DATA["providers"]
VERIFIED = DATA["verified"]


def max_verified(rows=None):
    # ponytail: freshness derived from the per-provider/model max — nightly probe keeps rows fresh; top-level "verified" is manual and goes stale
    vals = [v for p in (rows if rows is not None else ROWS)
            for v in [p.get("verified", ""), *(m.get("verified", "") for m in p["models"])] if v]
    return max(vals, default=VERIFIED)


VERIFIED_MAX = max_verified()
VERIFIED_HUMAN = date.fromisoformat(VERIFIED_MAX).strftime("%d %b %Y")
DATA_VERSION = hashlib.sha256(
    json.dumps(ROWS, sort_keys=True, ensure_ascii=False).encode()
).hexdigest()[:12]


def count_noun(n, noun):
    return f"{n} {noun if n == 1 else noun + 's'}"
TITLE = DATA["title"]
TAGLINE = DATA["tagline"]
AGENT_WARNING = ("Access varies per entry (`api_key`, `login`, or `bundled`) — a key does not work "
                 "for every provider; read the access field before assuming one.")
WEBSITE = DATA.get("website", "")
REPO = DATA.get("repo", "")

PLAUSIBLE = """<!-- Plausible Analytics -->
<script defer data-domain=\"freeinference.dev\" src=\"https://plausible.io/js/script.js\"></script>"""

CLARITY = """<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "yz5j1y2n6n");
</script>"""

KEY = {"Provider": "name", "Free tier": "free_type", "Free models": "models", "RPM": "rpm",
       "TPM": "tpm", "RPD": "rpd", "Day tokens": "tpd", "Context": "context",
       "Timeout": "timeout", "Notes": "notes"}

CHIP = {"Rate-limited free": "chip-free", "Promo free (limited time)": "chip-promo",
        "Trial credits": "chip-trial", "Rate-limited free (Free Trial)": "chip-trial",
        "Rate-limited free (Experiment)": "chip-trial"}


def cell(provider, col):
    v = provider.get(KEY[col], "—")
    if col == "Free models" and isinstance(v, list):
        v = ", ".join(m["name"] for m in v)
    return v


def row_md(p):
    return "| " + " | ".join(cell(p, c).replace("|", "\\|") for c in COLS) + " |"


def definitions():
    return {
        "RPM": "Requests per minute — API calls in any 60-second window.",
        "TPM": "Tokens per minute — input + output tokens across all calls in a minute.",
        "RPD": "Requests per day — hard daily cap, resets on the provider's clock.",
        "Day tokens": "Daily or periodic token/compute quota (some providers meter a token pool per day, month, or one-time credits instead).",
        "Timeout": "Max request duration before the provider kills the connection.",
        "Context": "Maximum context window available on the free tier.",
    }


def build_readme():
    total = sum(len(p["models"]) for p in ROWS)
    head = f"""# {TITLE}

{TAGLINE}

> **{VERIFIED_MAX}** · {count_noun(len(ROWS), 'provider')} · {count_noun(total, 'free model')}
> Interactive site: {WEBSITE} · Agent summary: {WEBSITE}/llms.txt · Machine data: {WEBSITE}/data/providers.json (validate against {WEBSITE}/data/schema.json)

## Providers

| Provider | Access | Free tier | Notable models | Notes |
| --- | --- | --- | --- | --- |
"""
    prov_rows = []
    for p in ROWS:
        name = f"[{p['name']}]({p['url']})"
        models = ", ".join(m["name"] for m in p["models"][:6])
        if len(p["models"]) > 6:
            models += f", +{len(p['models']) - 6} more"
        prov_rows.append(f"| {name} | {p.get('access_method', '—')} | {p['free_type']} | {models} | {p.get('notes', '—')} |")
    head += "\n".join(prov_rows) + "\n\n"

    sections = ["## Models (per provider)\n"]
    for p in ROWS:
        sections.append(f"### {p['name']}")
        sections.append("")
        sections.append("| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |")
        sections.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for m in p["models"]:
            sections.append("| " + " | ".join(
                html.escape(str(m[k])) for k in ("name", "cost", "context", "rpm", "tpm", "rpd", "tpd", "verified")
            ) + " |")
        sections.append("")

    tail = f"""## Definitions

| Term | Meaning |
| --- | --- |
"""
    tail += "\n".join(f"| {k} | {v} |" for k, v in definitions().items()) + "\n\n"
    tail += f"""## What counts as free

- **API-accessible** — an endpoint callable from a harness, agent, or CLI (key or keyless). Web-chat-only free tiers (ChatGPT, Claude.ai, Gemini app, deepseek.com, Grok, Copilot) are excluded on purpose.
- **Strictly $0** — no credit card for the free tier; expiring trial credits are flagged as such.
- Shapes: rate-limited free (forever, throttled), promo free (limited time), free gateways (OpenRouter, OpenCode Zen), trial credits (one-time).

## Caveats

Limits change without notice and vary per model, account age, region, peak hours. Treat this as a map, not a contract — verify before you architect on it.

## Maintain this catalog

Edit [`data/providers.json`](data/providers.json) (single source of truth), run `python3 build.py` to regenerate this README plus the site, open a PR with a primary-source link and verification date. Unverifiable rows are rejected. See [CONTRIBUTING.md](CONTRIBUTING.md).
"""
    return head + "\n".join(sections) + tail


def build_llms():
    site = WEBSITE.rstrip("/")
    total_models = sum(len(p["models"]) for p in ROWS)
    lines = [
        f"# {TITLE}",
        "",
        f"> {TAGLINE}",
        "",
        AGENT_WARNING,
        "",
        f"Last verified: {VERIFIED_MAX} · {count_noun(len(ROWS), 'provider')} · {count_noun(total_models, 'free model')}.",
        f"Data version: {DATA_VERSION} (changes only when catalog content changes).",
        "Verification methods: `live-probe` = checked against the provider's API nightly; `docs` = human-verified against official docs, stale-flagged after 45 days.",
        "",
        "## Catalog in every format",
        "",
        f"- [HTML + WebMCP]({site}/) — interactive catalog with browser-native WebMCP tools (`navigator.modelContext` / `search_models`, `get_provider`, `list_providers`, `compare_models`)",
        f"- [Markdown]({site}/index.md) — this entire catalog as one markdown document",
        f"- [JSON — full catalog]({site}/data/providers.json) — single source of truth",
        f"- [JSON Schema]({site}/data/schema.json) — validate before trusting",
        f"- [Per-provider JSON]({site}/data/<slug>.json) — one small file per provider:",
        "",
    ]
    lines += [f"  - [{p['name']}]({site}/data/{slug(p['name'])}.json)" for p in ROWS]
    lines += [
        "",
        "## Providers",
        "",
    ]
    for p in ROWS:
        models = ", ".join(m["name"] for m in p["models"])
        lines.append(f"- [{p['name']}]({p['url']}): access {p.get('access_method', '—')} · {p['free_type']} · {p['verified_method']} · verified {p['verified']} · models: {models}")
        for m in p["models"]:
            lines.append(
                f"  - {m['name']}: cost {m['cost']} · context {m['context']} · "
                f"RPM {m['rpm']} · TPM {m['tpm']} · RPD {m['rpd']} · day tokens {m['tpd']} · verified {m['verified']}"
            )
    lines += [
        "",
        "## Provider pages",
        "",
    ]
    lines += [f"- [{p['name']}]({site}/providers/{slug(p['name'])}/) · [markdown]({site}/providers/{slug(p['name'])}/index.md)" for p in ROWS]
    lines += [
        "",
        "## Free API Guides & Slices",
        "",
    ]
    lines += [f"- [{cfg['h1']}]({site}/{s}/) · [markdown]({site}/{s}/index.md)" for s, cfg in sorted(FREE_PAGES_CONFIG.items())]
    lines += [
        "",
        "## Definitions",
        "",
        *[f"- {k}: {v}" for k, v in definitions().items()],
        "",
        "## Caveats",
        "",
        "Limits change without notice and vary per model, account age, region, and peak hours. "
        "Treat this data as a map, not a contract — verify before you architect on it.",
    ]
    return "\n".join(lines) + "\n"


def build_schema():
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": TITLE,
        "type": "object",
        "required": ["title", "verified", "website", "columns", "providers"],
        "properties": {
            "title": {"type": "string"},
            "tagline": {"type": "string"},
            "verified": {"type": "string", "description": "ISO date of last verification"},
            "data_version": {"type": "string", "description": "Content fingerprint; changes only when catalog content changes"},
            "website": {"type": "string", "format": "uri"},
            "repo": {"type": "string"},
            "columns": {"type": "array", "items": {"type": "string"}},
            "providers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "url", "free_type", "verified", "models"],
                    "properties": {
                        "name": {"type": "string"},
                        "url": {"type": "string", "format": "uri"},
                        "free_type": {
                            "type": "string",
                            "enum": [
                                "Rate-limited free",
                                "Rate-limited free (Free Trial)",
                                "Rate-limited free (Experiment)",
                                "Promo free (limited time)",
                                "Trial credits",
                            ],
                        },
                        "notes": {"type": "string"},
                        "timeout": {"type": "string"},
                        "access_method": {"type": "string", "enum": ["api_key", "login", "bundled"]},
                        "artifact": {"type": "string"},
                        "base_url": {"type": "string"},
                        "verified": {"type": "string"},
                        "verified_method": {"type": "string", "enum": ["live-probe", "docs"]},
                        "models": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name", "cost", "context", "rpm", "tpm", "rpd", "tpd", "verified"],
                                "properties": {
                                    "name": {"type": "string"},
                                    "cost": {"type": "string"},
                                    "context": {"type": "string"},
                                    "rpm": {"type": "string"},
                                    "tpm": {"type": "string"},
                                    "rpd": {"type": "string"},
                                    "tpd": {"type": "string"},
                                    "verified": {"type": "string"},
                                },
                            },
                        },
                    },
                },
            },
        },
    }


CSS = '''  :root { --bg:#fff; --ink:#1a1a1a; --mut:#6b6b6b; --line:#e3e3e3; --sel:#111; --selink:#fff; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  a { color:var(--ink); }
  .wrap { max-width:1500px; margin:0 auto; padding:32px 24px 64px; }
  header { display:flex; align-items:baseline; gap:16px; border-bottom:1px solid var(--line);
           padding-bottom:16px; margin-bottom:20px; }
  h1 { font-size:24px; margin:0; letter-spacing:-.01em; }
  .tagline { color:var(--mut); margin:0; max-width:800px; font-size:15px; }
  .meta { color:var(--mut); font-size:13px; margin-left:auto; white-space:nowrap; }
  .layout { display:grid; grid-template-columns:280px 1fr; gap:20px; align-items:start; }
  @media (max-width:860px) { .layout { grid-template-columns:1fr; } .meta { display:none; } }
  .sidebar { border:1px solid var(--line); border-radius:8px; overflow:hidden;
              position:sticky; top:16px; background:var(--bg); }
  @media (max-width:860px) { .sidebar { position:static; } }
  #filter { width:100%; border:none; border-bottom:1px solid var(--line); padding:10px 14px;
            font:inherit; font-size:14px; outline:none; background:var(--bg); }
  #providers { max-height:74vh; overflow-y:auto; }
  .prow { display:block; width:100%; text-align:left; border:none; background:none; cursor:pointer;
           padding:10px 14px; border-bottom:1px solid var(--line); font:inherit; }
  .prow:hover { background:#f4f4f4; }
  .prow.active { background:var(--sel); color:var(--selink); }
  .prow .pname { font-weight:600; font-size:14px; display:block; }
  .prow .pmeta { font-size:12px; color:var(--mut); }
  .prow.active .pmeta { color:#bbb; }
  .dead { color:#b3261e; font-weight:700; }
  .prow.active .dead { color:#ff8a80; }
  .panel { border:1px solid var(--line); border-radius:8px; overflow:hidden; background:var(--bg); }
  .panel-head { padding:14px 18px; border-bottom:1px solid var(--line); }
  .panel-head h2 { margin:0 0 2px; font-size:19px; }
  .panel-head .ftype { font-size:12px; color:var(--mut); margin-left:8px; font-weight:400; }
  .amchip { font-size:11px; color:var(--mut); border:1px solid var(--line); border-radius:4px; padding:1px 6px; margin-left:8px; font-weight:400; vertical-align:middle; }
  .panel-head .purl { font-size:13px; color:var(--mut); }
  .panel-head .pnotes { font-size:13.5px; color:var(--ink); margin-top:6px; max-width:900px; }
  .table-wrap { overflow-x:auto; }
  table { border-collapse:collapse; width:100%; min-width:720px; font-size:13.5px; }
  th { text-align:left; padding:9px 12px; cursor:pointer; white-space:nowrap; user-select:none;
       border-bottom:1px solid var(--line); font-size:12px; text-transform:uppercase;
       letter-spacing:.03em; color:var(--mut); }
  th:hover { color:var(--ink); }
  td { border-bottom:1px solid var(--line); padding:8px 12px; vertical-align:top; }
  tr:last-child td { border-bottom:none; }
  tr:hover td { background:#f7f7f7; }
  td:first-child { font-weight:600; }
  .empty { padding:40px 20px; text-align:center; color:var(--mut); }
  .ftchips { border-top:1px solid var(--line); padding:12px 18px; font-size:13px; color:var(--mut); }
  #about { position:fixed; inset:0; background:rgba(0,0,0,.35); display:none; align-items:center;
            justify-content:center; z-index:10; }
  #about.open { display:flex; }
  .modal { background:var(--bg); max-width:640px; width:92%; max-height:82vh; overflow-y:auto;
            padding:26px 28px; border-radius:10px; }
  .modal h2 { margin:0 0 10px; font-size:18px; }
  .modal p, .modal li { font-size:14px; color:var(--ink); }
  .modal .x { position:absolute; };
  .close { float:right; border:1px solid var(--line); background:none; font:inherit; font-size:14px;
            cursor:pointer; padding:2px 10px; border-radius:6px; }
  footer { margin-top:32px; color:var(--mut); font-size:13px; }
  .fcols { display:grid; grid-template-columns:repeat(5,1fr); gap:20px 24px; text-align:left;
           margin:32px 0 14px; padding-top:22px; border-top:1px solid var(--line); }
  .fcol h3 { margin:0 0 8px; font-size:12px; text-transform:uppercase; letter-spacing:.04em;
             color:var(--ink); font-weight:600; }
  .fcol ul { list-style:none; margin:0; padding:0; }
  .fcol li { margin:4px 0; font-size:13px; }
  .fcol a { color:var(--mut); text-decoration:none; }
  .fcol a:hover { color:var(--ink); text-decoration:underline; }
  .fnote { font-size:12px; color:var(--mut); margin:0 0 8px; }
  .answer { border:1px solid var(--line); border-radius:10px; padding:16px 18px; margin:20px 0 4px; }
  .answer h2 { margin:0 0 8px; font-size:16px; }
  .answer p { margin:0 0 8px; font-size:14px; }
  .answer ul { margin:0 0 8px; padding-left:18px; font-size:14px; }
  .answer li { margin:3px 0; }
  .answer-more { color:var(--mut); font-size:13px; margin:0; }
  .code-box { background:#f8f9fa; border:1px solid var(--line); border-radius:6px; padding:12px 16px; font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:13px; overflow-x:auto; margin:10px 0; }
  .code-box code { font-family:inherit; }
  .quick-connect { border:1px solid var(--line); border-radius:8px; padding:16px 18px; margin:20px 0; background:#fafafa; }
  .quick-connect h2 { margin:0 0 8px; font-size:16px; }
  .quick-connect p { margin:0 0 8px; font-size:14px; }
  .models { margin-top:24px; }
  .models h2 { margin:0 0 12px; font-size:17px; }
  @media (max-width:860px) { .fcols { grid-template-columns:repeat(2,1fr); } }'''


FOOTER_GROUPS = [
    ("Coding tools", ["github-copilot--free", "cursor--hobby", "windsurf", "kiro--aws",
                      "trae--bytedance", "bolt-new", "lovable", "v0--vercel", "replit--starter"]),
    ("Labs & clouds", ["google-ai-studio--gemini-api", "mistral-la-plateforme",
                       "nvidia-nim--build-nvidia-com", "cohere", "together-ai",
                       "sambanova-cloud", "deepinfra", "cloudflare-workers-ai", "hugging-face"]),
    ("Gateways & keys", ["openrouter", "groq", "cerebras", "z-ai--zhipu", "requesty",
                         "ovhcloud-ai-endpoints", "nous-portal", "kilo-gateway", "opencode-zen",
                         "siliconflow", "deepseek-platform"]),
    ("Builders & notebooks", ["kaggle-notebooks", "hugging-face-spaces", "google-colab",
                              "figma--starter", "canva--free", "framer--free", "devin--free",
                              "qoder", "antigravity-cli--google"]),
]


def footer_nav(verified):
    by_slug = {slug(p["name"]): p for p in ROWS}
    grouped, cols = set(), []
    for label, slugs in FOOTER_GROUPS:
        items = []
        for s in slugs:
            p = by_slug.get(s)
            if p:
                grouped.add(s)
                items.append(f'<li><a href="/providers/{s}/">{html.escape(p["name"])}</a></li>')
        if items:
            cols.append(f'<div class="fcol"><h3>{label}</h3><ul>{"".join(items)}</ul></div>')
    leftovers = [s for s in by_slug if s not in grouped]
    if leftovers:
        items = "".join(f'<li><a href="/providers/{s}/">{html.escape(by_slug[s]["name"])}</a></li>'
                        for s in leftovers)
        cols.append(f'<div class="fcol"><h3>More providers</h3><ul>{items}</ul></div>')
    cols.append('<div class="fcol"><h3>Machine access</h3><ul>'
                '<li><a href="/llms.txt">llms.txt</a></li>'
                '<li><a href="/index.md">index.md</a></li>'
                '<li><a href="/data/providers.json">providers.json</a></li>'
                '<li><a href="/data/schema.json">schema.json</a></li>'
                '<li><a href="/sitemap.xml">sitemap.xml</a></li></ul></div>')
    total_models = sum(len(p["models"]) for p in ROWS)
    return ('<nav class="fcols" aria-label="All providers">' + "".join(cols) + '</nav>'
            f'<p class="fnote">{count_noun(len(ROWS), "provider")} · {count_noun(total_models, "model")} · '
            f'verified {html.escape(verified)}. Limits change without notice — this is a map, not a contract.</p>')


def answer_block():
    total_models = sum(len(p["models"]) for p in ROWS)
    ranked = sorted(ROWS, key=lambda p: len(p["models"]), reverse=True)
    widest = ranked[0]
    api = next((p for p in ranked if p.get("access_method") == "api_key" and p is not widest), None)
    tool = next((p for p in ranked if p.get("access_method") in ("login", "bundled")), None)

    def item(label, p, note):
        return (f'<li><strong>{label}:</strong> '
                f'<a href="/providers/{slug(p["name"])}/">{html.escape(p["name"])}</a> — {note}</li>')

    items = [item("Widest choice", widest, f'{count_noun(len(widest["models"]), "free model")} in one place')]
    if api:
        items.append(item("Direct API key", api, f'{count_noun(len(api["models"]), "free model")}, callable with a key'))
    if tool:
        items.append(item("Coding tool", tool, f'{count_noun(len(tool["models"]), "free model")}, {tool.get("access_method")} access'))
    return f"""<section class="answer">
  <h2>Which free LLM API should I use?</h2>
  <p>Free LLM inference you can build with: {count_noun(len(ROWS), "provider")}, {count_noun(total_models, "model")}, no card for most entries. Pick by how you get in:</p>
  <ul>
    {"".join(items)}
  </ul>
  <p class="answer-more">Every provider is listed below, with a detail page for limits and how to get in.</p>
</section>"""


def build_html():
    total_models = sum(len(p["models"]) for p in ROWS)
    provider_count = len(ROWS)

    page_title = f"FreeInference.dev — Free LLM API Directory: {count_noun(total_models, 'Model')}, {count_noun(provider_count, 'Provider')}, Updated {VERIFIED_HUMAN}"
    meta_desc = (f"{count_noun(total_models, 'free LLM model')}, {count_noun(provider_count, 'provider')} — an API key, a CLI login, "
                 f"or inference bundled in an IDE. No credit card required. Updated {VERIFIED_HUMAN}.")

    head_title = html.escape(page_title)
    head_desc = html.escape(meta_desc)
    data_json = json.dumps(DATA, ensure_ascii=False, indent=1)
    verified = html.escape(VERIFIED_MAX)
    website = html.escape(WEBSITE)
    footer = footer_nav(verified)
    answer = answer_block()
    tagline = html.escape(TAGLINE)
    defs = "\n".join(f"<p><strong>{html.escape(k)}</strong> — {html.escape(v)}</p>" for k, v in definitions().items())
    t = TITLE.lower()

    thead = "".join(f"<th><span>{html.escape(c)}</span></th>" for c in COLS)
    body = "".join(row_html(p) for p in ROWS)

    # ponytail: inline gtag when ga_measurement_id set in providers.json; no consent banner (no cookies set by default config)
    ga_id = DATA.get("ga_measurement_id", "")
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>\n'
          f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}};'
          f"gtag('js',new Date());gtag('config','{ga_id}');</script>") if ga_id else ""

    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": TITLE,
        "description": meta_desc,
        "url": WEBSITE,
        "dateModified": VERIFIED_MAX,
        "version": DATA_VERSION,
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": f"{WEBSITE}/data/providers.json"},
            {"@type": "DataDownload", "encodingFormat": "application/schema+json",
             "contentUrl": f"{WEBSITE}/data/schema.json"},
            {"@type": "DataDownload", "encodingFormat": "text/plain",
             "contentUrl": f"{WEBSITE}/llms.txt"},
        ],
        "license": "https://opensource.org/licenses/MIT",
        **({"sameAs": REPO} if REPO else {}),
        "keywords": ["free LLM API", "inference providers", "rate limits", "AI agents", "WebMCP", "llms.txt"],
        "variableMeasured": ["RPM", "TPM", "RPD", "Context Window", "Daily Token Limits", "Model Pricing"],
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }
    }, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{head_title}</title>
<meta name="description" content="{head_desc}">
<meta name="data-version" content="{DATA_VERSION}">
<link rel="canonical" href="{website}">
<link rel="alternate" type="text/markdown" href="{website}/index.md">
<link rel="alternate" type="text/plain" title="LLM summary" href="{website}/llms.txt">

<!-- OpenGraph / Social Metadata -->
<meta property="og:site_name" content="{html.escape(TITLE)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{website}">
<meta property="og:title" content="{head_title}">
<meta property="og:description" content="{head_desc}">
<meta property="og:updated_time" content="{verified}T00:00:00Z">

<!-- Twitter / X Metadata -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{head_title}">
<meta name="twitter:description" content="{head_desc}">

<link rel="icon" href="data:,">
{ga}
{PLAUSIBLE}\n{CLARITY}
<script type="application/ld+json">{ld}</script>
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Free Inference You Can Build With</h1>
    <p class="tagline">{tagline}</p>
    <span class="meta">verified {verified} · <a href="#about" id="aboutlink">about / contribute</a></span>
  </header>

  {answer}

  <noscript>
    <div class="table-wrap">
      <table><thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table>
    </div>
  </noscript>

  <div id="app" class="layout"></div>

  <footer>
  {footer}
  </footer>
</div>

<div id="about" role="dialog" aria-modal="true">
  <div class="modal">
    <button class="close">close</button>
    <h2>About {html.escape(TITLE)}</h2>
    <p><strong>What is here:</strong> every entry gives you free access to LLM inference you can build
    with. That access comes one of three ways: an <strong>API key</strong> you call directly, a
    <strong>login</strong> to a CLI or tool that carries the model, or inference <strong>bundled</strong>
    inside a coding tool or builder. Each entry states which, because a key isn't always the way in.</p>
    <p>The test for inclusion is whether you can produce an artifact you keep: code, an app, a website,
    a design, an agent, a skill. Converse-only free tiers (ChatGPT, Claude.ai, Gemini app, deepseek.com,
    Grok, Copilot) are excluded on purpose — they don't give you something to build with.</p>
    <p><strong>What counts as free:</strong> strictly $0. No entry requires a credit card, ever.
    Expiring trial credits are flagged as such in the cost column rather than presented as a standing
    free tier.</p>
    <p>Free takes four shapes here: rate-limited free (forever, throttled), promo free (limited time),
    free gateways (OpenRouter, OpenCode Zen), and trial credits (one-time, expires). Verification is
    mixed and honest about it: rows are checked by a nightly live probe where the provider exposes an
    API, and by hand against official docs where it doesn't. The date on a row is when we last checked
    it, not a guarantee it holds tomorrow. Limits move without notice. This is a map, not a contract.</p>
    <h2>Definitions</h2>
    {defs}
    <h2>Agent access</h2>
    <ul>
      <li>Machine data: <a href="data/providers.json" rel="noopener">data/providers.json</a> — validate
      against <a href="data/schema.json" rel="noopener">data/schema.json</a></li>
      <li>Agent summary: <a href="llms.txt" rel="noopener">llms.txt</a></li>
      <li>WebMCP: Browser-native tools registered via <code>navigator.modelContext</code> (<code>search_models</code>, <code>get_provider</code>, <code>list_providers</code>, <code>compare_models</code>)</li>
      <li>This page and the repo README are generated from that one file — edit the JSON, run
      <code>python3 build.py</code>, done.</li>
    </ul>
    <h2>Contribute</h2>
    <p>Add or correct a row in <code>data/providers.json</code> with a link to your official limits
    page and the date it was verified, then open a PR. Unverifiable rows get rejected.</p>
  </div>
</div>

<script>
const DATA = {data_json};
const DEFS = {json.dumps(definitions(), ensure_ascii=False)};

function modelRow(m) {{
  return `<tr><td>${{m.name}}</td><td>${{m.cost}}</td><td>${{m.context}}</td>
    <td>${{m.rpm}}</td><td>${{m.tpm}}</td><td>${{m.rpd}}</td>
    <td>${{m.tpd}}</td><td>${{m.verified}}</td></tr>`;
}}

function trackMcpCall(toolName, params) {{
  if (typeof window.gtag === "function") {{
    window.gtag("event", "webmcp_tool_call", {{
      tool_name: toolName,
      search_query: params.query || "",
      provider_param: params.provider_name || params.provider || "",
      model_count: Array.isArray(params.model_names) ? params.model_names.length : undefined
    }});
  }}
}}

const tools = {{
  search_models: {{
    name: "search_models",
    description: "Search free LLM models by keyword, minimum context length, provider name, or free tier type.",
    inputSchema: {{
      type: "object",
      properties: {{
        query: {{ type: "string", description: "Search query across model name or provider" }},
        min_context_k: {{ type: "number", description: "Minimum context window in thousands (e.g. 128 for 128K+)" }},
        provider: {{ type: "string", description: "Filter by provider name (partial or exact)" }},
        free_type: {{ type: "string", description: "Filter by free tier type (e.g. 'Rate-limited free', 'Promo free (limited time)', 'Trial credits')" }}
      }}
    }},
    execute: async (params = {{}}) => {{
      trackMcpCall("search_models", params);
      const q = (params.query || "").toLowerCase();
      const pFilter = (params.provider || "").toLowerCase();
      const ftFilter = (params.free_type || "").toLowerCase();
      const minCtx = params.min_context_k || 0;
      const results = [];
      for (const prov of DATA.providers) {{
        if (pFilter && !prov.name.toLowerCase().includes(pFilter)) continue;
        if (ftFilter && !prov.free_type.toLowerCase().includes(ftFilter)) continue;
        for (const m of prov.models) {{
          const nameMatch = !q || m.name.toLowerCase().includes(q) || prov.name.toLowerCase().includes(q);
          let ctxNum = 0;
          const ctxMatch = String(m.context).match(/(\\d+)K?/i);
          if (ctxMatch) {{
            ctxNum = parseInt(ctxMatch[1], 10);
            if (!String(m.context).toUpperCase().includes("K") && ctxNum > 1000) ctxNum = Math.floor(ctxNum / 1024);
          }}
          const passCtx = minCtx === 0 || ctxNum >= minCtx;
          if (nameMatch && passCtx) {{
            results.push({{
              provider: prov.name,
              free_type: prov.free_type,
              model: m.name,
              cost: m.cost,
              context: m.context,
              rpm: m.rpm,
              tpm: m.tpm,
              rpd: m.rpd,
              tpd: m.tpd,
              verified: m.verified
            }});
          }}
        }}
      }}
      return results;
    }}
  }},
  get_provider: {{
    name: "get_provider",
    description: "Get comprehensive details and model inventory for a specific free inference provider.",
    inputSchema: {{
      type: "object",
      properties: {{
        provider_name: {{ type: "string", description: "Exact or partial provider name (e.g. 'Google', 'Groq', 'OpenRouter', 'OpenCode Zen')" }}
      }},
      required: ["provider_name"]
    }},
    execute: async (params = {{}}) => {{
      trackMcpCall("get_provider", params);
      const target = (params.provider_name || "").toLowerCase();
      const found = DATA.providers.find(p => p.name.toLowerCase().includes(target));
      if (!found) return {{ error: `Provider '${{params.provider_name}}' not found in catalog.` }};
      return found;
    }}
  }},
  list_providers: {{
    name: "list_providers",
    description: "List all free LLM inference providers with summary metadata, free tier type, and model counts.",
    inputSchema: {{
      type: "object",
      properties: {{
        free_type: {{ type: "string", description: "Optional filter by free tier type" }}
      }}
    }},
    execute: async (params = {{}}) => {{
      trackMcpCall("list_providers", params);
      const ft = (params.free_type || "").toLowerCase();
      return DATA.providers
        .filter(p => !ft || p.free_type.toLowerCase().includes(ft))
        .map(p => ({{
          name: p.name,
          url: p.url,
          free_type: p.free_type,
          model_count: p.models.length,
          verified: p.verified,
          verified_method: p.verified_method,
          notes: p.notes
        }}));
    }}
  }},
  compare_models: {{
    name: "compare_models",
    description: "Compare rate limits and specs of specific models across providers.",
    inputSchema: {{
      type: "object",
      properties: {{
        model_names: {{ type: "array", items: {{ type: "string" }}, description: "Array of model names to compare" }}
      }},
      required: ["model_names"]
    }},
    execute: async (params = {{}}) => {{
      trackMcpCall("compare_models", params);
      const names = (params.model_names || []).map(n => n.toLowerCase());
      const matches = [];
      for (const p of DATA.providers) {{
        for (const m of p.models) {{
          if (names.some(n => m.name.toLowerCase().includes(n) || n.includes(m.name.toLowerCase()))) {{
            matches.push({{
              provider: p.name,
              model: m.name,
              cost: m.cost,
              context: m.context,
              rpm: m.rpm,
              tpm: m.tpm,
              rpd: m.rpd,
              tpd: m.tpd,
              verified: m.verified
            }});
          }}
        }}
      }}
      return matches;
    }}
  }}
}};

function registerWebMcp() {{
  const mc = navigator.modelContext || window.modelContext || (typeof document !== "undefined" && document.modelContext);
  if (mc && typeof mc.registerTool === "function") {{
    for (const tool of Object.values(tools)) {{
      try {{
        mc.registerTool({{
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema,
          execute: tool.execute,
          annotations: {{ readOnlyHint: true }}
        }});
      }} catch (e) {{
        console.warn("WebMCP registration failed:", tool.name, e);
      }}
    }}
  }}
}}

window.freeInferenceTools = tools;
window.webmcp = tools;
registerWebMcp();

const AM = {{api_key:"API key", login:"Login", bundled:"Bundled"}};
const plural = (n, one) => n + " " + one + (n === 1 ? "" : "s");

function render(app) {{
  const list = DATA.providers;
  let activeIdx = 0, filter = "", rows = [...list];
  const sidebar = document.createElement("div");
  sidebar.className = "sidebar";
  const panel = document.createElement("div");
  panel.className = "panel";
  app.append(sidebar, panel);

  sidebar.innerHTML = `<input id="filter" type="text" placeholder="Filter provider or model…" autocomplete="off">
    <div id="providers"></div>`;
  const providersEl = sidebar.querySelector("#providers");
  const filterEl = sidebar.querySelector("#filter");

  function drawSidebar() {{
    rows = list.filter(p => !filter ||
      (p.name + " " + p.models.map(m => m.name).join(" ")).toLowerCase().includes(filter.toLowerCase()));
    providersEl.innerHTML = rows.map((p, i) => {{
      const active = list.indexOf(p) === activeIdx ? " active" : "";
      const dead = p.dead ? ` <span class="dead">• dead</span>` : "";
      return `<button class="prow${{active}}" data-i="${{i}}">
        <span class="pname">${{p.name}}${{dead}}</span>
        <span class="pmeta">${{p.free_type}} · ${{plural(p.models.length, "free model")}} · ${{AM[p.access_method] || p.access_method}}</span></button>`;
    }}).join("");
    providersEl.querySelectorAll(".prow").forEach(b =>
      b.addEventListener("click", () => {{ activeIdx = list.indexOf(rows[+b.dataset.i]); drawPanel(); drawSidebar(); }}));
    if (!rows.length) providersEl.innerHTML = `<div class="empty">No match.</div>`;
  }}

  function drawPanel() {{
    const p = list[activeIdx];
    const dead = p.dead ? `<div class="pnotes"><strong class="dead">Probe flags this provider unreachable — verify before relying on it.</strong></div>` : "";
    panel.innerHTML = `<div class="panel-head">
      <h2>${{p.name}}<span class="ftype">${{p.free_type}}</span><span class="amchip">${{AM[p.access_method] || p.access_method}}</span></h2>
      <a class="purl" href="${{p.url}}" target="_blank" rel="noopener">${{p.url}}</a>
      <div class="pnotes">${{p.notes}}</div>
      <div class="pnotes"><strong>Last updated: ${{p.verified}}</strong>${{p.verified_method === "docs" ? " · verified against official public documentation" : " · verified nightly via automated probe"}}</div>${{dead}}
    </div>
    <div class="table-wrap"><table>
      <thead><tr><th data-k="name">Model</th><th data-k="cost">Cost</th><th data-k="context">Context</th>
      <th data-k="rpm">RPM</th><th data-k="tpm">TPM</th><th data-k="rpd">RPD</th>
      <th data-k="tpd">Day tokens</th><th data-k="verified">Verified</th></tr></thead>
      <tbody id="mtbody">${{p.models.map(modelRow).join("")}}</tbody>
    </table></div>`;

    let asc = true, lastKey = "";
    panel.querySelectorAll("th").forEach(th => th.addEventListener("click", () => {{
      const k = th.dataset.k;
      if (lastKey === k) asc = !asc; else {{ lastKey = k; asc = true; }}
      const ms = [...p.models].sort((a, b) =>
        String(a[k]).localeCompare(String(b[k]), undefined, {{ numeric: true }}));
      if (!asc) ms.reverse();
      panel.querySelector("#mtbody").innerHTML = ms.map(modelRow).join("");
    }}));
  }}

  filterEl.addEventListener("input", () => {{ filter = filterEl.value.trim(); drawSidebar(); }});
  drawSidebar(); drawPanel();
}}

document.addEventListener("DOMContentLoaded", () => render(document.getElementById("app")));

const m = document.getElementById("about");
document.getElementById("aboutlink").addEventListener("click", e => {{ e.preventDefault(); m.classList.add("open"); }});
m.querySelector(".close").addEventListener("click", () => m.classList.remove("open"));
m.addEventListener("click", e => {{ if (e.target === m) m.classList.remove("open"); }});
document.addEventListener("keydown", e => {{ if (e.key === "Escape") m.classList.remove("open"); }});
</script>
</body>
</html>
"""


def row_html(p):
    name = html.escape(p["name"])
    tds = "".join(f"<td>{html.escape(str(cell(p, c)))}</td>" for c in COLS[1:])
    return f'<tr><td><a href="{html.escape(p["url"])}" target="_blank" rel="noopener">{name}</a></td>{tds}</tr>'


def slug(name):
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


ACCESS_LABEL = {"api_key": "API key", "login": "Login", "bundled": "Bundled"}
ACCESS_PROSE = {"api_key": "API key", "login": "login", "bundled": "bundled"}

def parse_ctx_val(ctx_str):
    m = re.match(r"(\d+)([KM]?)", str(ctx_str).upper())
    if not m:
        return 0
    val, unit = int(m.group(1)), m.group(2)
    return val * 1024 if unit == "M" else (val if unit == "K" else val // 1024)


def clean_ctx_token(ctx_str):
    c = str(ctx_str).strip()
    if not c or c == "—" or "model-dependent" in c.lower() or "varies" in c.lower():
        return ""
    m = re.search(r"\d+[KM]?", c.upper())
    return m.group(0) if m else ""


def generate_provider_descriptions(p, verified_human):
    count = len(p["models"])
    m_count = f"{count} free model{'s' if count != 1 else ''}"

    # Clean model names: strip :free suffix, parens, and trim
    m_names = []
    for m in p["models"][:3]:
        raw = m["name"].replace(":free", "")
        cleaned = re.sub(r"\(.*?\)", "", raw).strip()
        m_names.append(cleaned if cleaned else raw)

    # Max context
    contexts = [clean_ctx_token(m.get("context", "")) for m in p["models"]]
    contexts = [c for c in contexts if c]
    best_ctx = max(contexts, key=parse_ctx_val) if contexts else ""
    ctx_str = f"up to {best_ctx} context" if best_ctx else ""

    # Card / Billing requirement
    notes_lower = p.get("notes", "").lower()
    if "no credit card" in notes_lower or "no card" in notes_lower:
        card_long = "no credit card required"
        card_short = "no card needed"
    elif "card required" in notes_lower or "credit card required" in notes_lower:
        card_long = "credit card required"
        card_short = "card required"
    else:
        card_long = ""
        card_short = ""

    # Protocol & endpoint
    endpoint = p.get("base_url", "")
    if not endpoint:
        url_m = re.search(r"https?://[^\s\),]+", p.get("notes", ""))
        endpoint = url_m.group(0).rstrip(".") if url_m else ""

    if "openai-compatible" in notes_lower and endpoint:
        proto_og = f"OpenAI-compatible endpoint ({endpoint})"
        proto_meta = "OpenAI API"
    elif "openai-compatible" in notes_lower:
        proto_og = "OpenAI-compatible endpoint"
        proto_meta = "OpenAI API"
    elif endpoint:
        proto_og = f"API endpoint ({endpoint})"
        proto_meta = "API key"
    elif p.get("access_method") == "api_key":
        proto_og = "API key access"
        proto_meta = "API key"
    elif p.get("access_method") == "login":
        proto_og = "Web / CLI login access"
        proto_meta = "login access"
    else:
        proto_og = "Bundled app access"
        proto_meta = "bundled"

    # Surface 1: SEO Meta Description (Target: 150-160 chars)
    if count > 1 and m_names:
        models_meta = f"({', '.join(m_names[:2])})"
    elif count == 1 and m_names:
        models_meta = f"({m_names[0]})"
    else:
        models_meta = ""
    parts_meta = [f"{m_count} on {p['name']}"]
    if models_meta:
        parts_meta[0] += f" {models_meta}"
    dtls_meta = [d for d in [proto_meta, ctx_str, card_short] if d]
    meta_desc = f"{parts_meta[0]}. {', '.join(dtls_meta)}. Last updated: {verified_human}."

    # Surface 2: Social & Agent OG Description (Target: 200-260 chars)
    if count > 2:
        models_og = f"including {', '.join(m_names[:2])}, and {m_names[2]}"
    elif count == 2:
        models_og = f"including {m_names[0]} and {m_names[1]}"
    elif count == 1:
        models_og = f"({m_names[0]})"
    else:
        models_og = ""
    parts_og = [f"{m_count} on {p['name']}"]
    if models_og:
        parts_og[0] += f" {models_og}"
    dtls_og = [d for d in [proto_og, ctx_str, card_long] if d]
    og_desc = f"{parts_og[0]}. {', '.join(dtls_og)}. Last updated: {verified_human}."

    # Adaptive clamp if endpoint URL pushed OG beyond 260 chars
    if len(og_desc) > 260 and endpoint:
        proto_og = "OpenAI-compatible endpoint" if "openai-compatible" in notes_lower else "API key access"
        dtls_og = [d for d in [proto_og, ctx_str, card_long] if d]
        og_desc = f"{parts_og[0]}. {', '.join(dtls_og)}. Last updated: {verified_human}."

    return meta_desc, og_desc


def model_row_html(m):
    e = html.escape
    cells = "".join(f"<td>{e(str(m[k]))}</td>" for k in
                    ("name", "cost", "context", "rpm", "tpm", "rpd", "tpd", "verified"))
    return f"<tr>{cells}</tr>"


def build_provider_page(p):
    name = html.escape(p["name"])
    s = slug(p["name"])
    access = p.get("access_method", "api_key")
    access_label = ACCESS_LABEL.get(access, access)
    artifact = html.escape(str(p.get("artifact", "—")))
    free_type = html.escape(p["free_type"])
    p_max = max_verified([p])
    verified = html.escape(p_max)
    footer = footer_nav(verified)
    verified_human = date.fromisoformat(p_max).strftime("%d %b %Y")
    verified_month = date.fromisoformat(p_max).strftime("%b %Y")
    page_url = f"{WEBSITE.rstrip('/')}/providers/{s}/"
    count = len(p["models"])
    title = f"{p['name']} Free Tier: {count_noun(count, 'Model')}, Rate Limits ({verified_month})"
    meta_desc, og_desc = generate_provider_descriptions(p, verified_human)
    docs = html.escape(p.get("docs_url", p["url"]))
    notes = html.escape(p.get("notes", ""))
    notes_html = f"<p>{notes}</p>" if notes else ""
    rows = "\n".join(model_row_html(m) for m in p["models"])
    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": og_desc,
        "dateModified": p["verified"],
        "version": DATA_VERSION,
        "isPartOf": {"@type": "Dataset", "name": TITLE, "url": WEBSITE},
        "about": {"@type": "Thing", "name": p["name"], "url": p["url"]},
    }, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(meta_desc)}">
<meta name="data-version" content="{DATA_VERSION}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" type="text/markdown" href="{page_url}index.md">

<meta property="og:site_name" content="{html.escape(TITLE)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(og_desc)}">
<meta property="og:updated_time" content="{verified}T00:00:00Z">

<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(og_desc)}">

<link rel="icon" href="data:,">
{PLAUSIBLE}\n{CLARITY}
<script type="application/ld+json">{ld}</script>
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{name}</h1>
    <p class="tagline">{free_type} · {access_label} · {artifact} · Last updated: {verified_human}</p>
    <span class="meta"><a href="/">← back to the directory</a></span>
  </header>

  <p><strong>{html.escape(og_desc)}</strong></p>
  {notes_html}
  <p>Source: <a href="{docs}" target="_blank" rel="noopener">{docs}</a> · Last updated: {verified_human}</p>

  <div class="table-wrap"><table>
    <thead><tr><th>Model</th><th>Cost</th><th>Context</th><th>RPM</th><th>TPM</th><th>RPD</th><th>Day tokens</th><th>Verified</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table></div>

  <p>Machine-readable: <a href="/data/{s}.json">/data/{s}.json</a> · <a href="/providers/{s}/index.md">Markdown</a></p>
  <p><a href="/">← back to the directory</a></p>

  <footer>
  {footer}
  </footer>
</div>
</body>
</html>
"""


def build_provider_md(p):
    s = slug(p["name"])
    access = p.get("access_method", "api_key")
    access_label = ACCESS_LABEL.get(access, access)
    p_max = max_verified([p])
    verified_human = date.fromisoformat(p_max).strftime("%d %b %Y")
    meta_desc, og_desc = generate_provider_descriptions(p, verified_human)
    lines = [
        f"# {p['name']}",
        "",
        f"{p['free_type']} · {access_label} · {p.get('artifact', '—')} · Last updated: {verified_human}",
        "",
        og_desc,
        "",
    ]
    if p.get("notes"):
        lines.extend([p["notes"], ""])
    lines.extend([
        f"Source: {p.get('docs_url', p['url'])} · Last updated: {verified_human}",
        "",
        "| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for m in p["models"]:
        cells = " | ".join(str(m[k]).replace("|", "\\|") for k in
                           ("name", "cost", "context", "rpm", "tpm", "rpd", "tpd", "verified"))
        lines.append(f"| {cells} |")
    lines += [
        "",
        f"Machine-readable: /data/{s}.json",
        "",
        f"Numbers cross-checked against official docs and third-party trackers as of {p_max}. Limits change without notice — this is a map, not a contract.",
    ]
    return "\n".join(lines) + "\n"


def build_index_md():
    site = WEBSITE.rstrip("/")
    md = build_readme()
    md = md.replace(f"{TAGLINE}\n", f"{TAGLINE}\n\n{AGENT_WARNING}\n", 1)
    for rel in ("data/providers.json", "CONTRIBUTING.md"):
        md = md.replace(f"]({rel})", f"]({site}/{rel})")
    return md


FREE_PAGES_CONFIG = {
    "free-deepseek-api": {
        "title": "Free DeepSeek API — $0 Endpoints, Rate Limits & Keys (2026)",
        "h1": "Free DeepSeek API Endpoints & Rate Limits",
        "bluf": "Free DeepSeek API access is available via SambaNova Cloud (DeepSeek-V3.1 & V3.2), DeepInfra, and Cloudflare Workers AI. No credit card is required on rate-limited tiers.",
        "desc": "Directory of free DeepSeek API endpoints. Rate limits, context windows, and base URLs for DeepSeek-V3.1, V3.2, and distills without credit card.",
        "filter": lambda p, m: "deepseek" in m["name"].lower() or "deepseek" in p["name"].lower(),
        "tool_snippet": {
            "base_url": "https://api.sambanova.ai/v1",
            "model": "DeepSeek-V3.2",
            "provider": "SambaNova Cloud",
            "notes": "Direct OpenAI-compatible base URL for free DeepSeek-V3.2 inference."
        }
    },
    "free-glm-api": {
        "title": "Free GLM API — $0 Zhipu Endpoints, Rate Limits & Keys (2026)",
        "h1": "Free GLM API Endpoints & Rate Limits",
        "bluf": "Free GLM API inference is provided directly by Z.AI (Zhipu BigModel) with GLM-5.1, GLM-4.7-Flash, and GLM-4.6V-Flash, as well as NVIDIA NIM and Kilo Gateway with OpenAI-compatible endpoints.",
        "desc": "Free GLM API directory. Rate limits, context windows, and base URLs for GLM-5.1, GLM-4.7-Flash, and GLM-4.6V without paying subscription fees.",
        "filter": lambda p, m: "glm" in m["name"].lower() or "zhipu" in p["name"].lower() or "z.ai" in p["name"].lower(),
        "tool_snippet": {
            "base_url": "https://open.bigmodel.cn/api/paas/v4/",
            "model": "GLM-4.7-Flash",
            "provider": "Z.AI (Zhipu)",
            "notes": "OpenAI-compatible endpoint for free GLM-4.7-Flash inference."
        }
    },
    "free-qwen-api": {
        "title": "Free Qwen API — $0 Alibaba Qwen Endpoints & Rate Limits (2026)",
        "h1": "Free Qwen API Endpoints & Rate Limits",
        "bluf": "Free Qwen API inference is available through Groq (Qwen 3.8 27B at ultra-high speed), Cerebras ($5 trial), DeepInfra, and Hugging Face Serverless with standard OpenAI compatibility.",
        "desc": "Compare free Qwen API providers. Rate limits, context windows, and token quotas for Qwen 3.8, Qwen 2.5 Coder, and 72B open models.",
        "filter": lambda p, m: "qwen" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "qwen/qwen3.8-27b",
            "provider": "Groq",
            "notes": "Sub-second latency Qwen 3.8 27B inference via Groq LPU."
        }
    },
    "free-llama-api": {
        "title": "Free Llama API — $0 Meta Llama 3.3 Endpoints & Limits (2026)",
        "h1": "Free Llama API Endpoints & Rate Limits",
        "bluf": "Free Llama API access is hosted by SambaNova Cloud (Llama 3.3 70B Instruct at high throughput), Groq, Cloudflare Workers AI, and Hugging Face with zero credit card required.",
        "desc": "Directory of free Meta Llama API endpoints. Rate limits and context windows for Llama 3.3 70B, Llama 3.2 8B, and Guard models.",
        "filter": lambda p, m: "llama" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://api.sambanova.ai/v1",
            "model": "Meta-Llama-3.3-70B-Instruct",
            "provider": "SambaNova Cloud",
            "notes": "High-throughput Llama 3.3 70B Instruct via SambaNova Cloud."
        }
    },
    "free-gemini-api": {
        "title": "Free Gemini API — Google AI Studio Endpoints & Limits (2026)",
        "h1": "Free Gemini API Endpoints & Rate Limits",
        "bluf": "Google AI Studio provides 14 free Gemini models (including Gemini 2.5 Flash, 3.5 Flash, and Flash-Lite) with 1M context windows, up to 15 RPM, and an official OpenAI-compatible endpoint.",
        "desc": "Complete reference for Google AI Studio free Gemini API tier. Verified RPM, TPM, RPD, and 1M context limits across all Gemini models.",
        "filter": lambda p, m: "gemini" in m["name"].lower() or "google ai studio" in p["name"].lower(),
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-2.5-flash",
            "provider": "Google AI Studio (Gemini API)",
            "notes": "Official Google AI Studio OpenAI-compatible endpoint with 1M context."
        }
    },
    "free-mistral-api": {
        "title": "Free Mistral API — $0 Codestral & Large Endpoints (2026)",
        "h1": "Free Mistral API Endpoints & Rate Limits",
        "bluf": "Mistral La Plateforme offers free experiment tier API keys for Codestral and Mistral Large with 1 req/sec and 1B tokens/month without requiring a credit card.",
        "desc": "Directory of free Mistral API keys. Rate limits and token allowances for Codestral, Mistral Large, and Mistral 7B.",
        "filter": lambda p, m: "mistral" in m["name"].lower() or "codestral" in m["name"].lower() or "mistral" in p["name"].lower(),
        "tool_snippet": {
            "base_url": "https://api.mistral.ai/v1",
            "model": "Codestral",
            "provider": "Mistral La Plateforme",
            "notes": "Codestral endpoint with 1B free tokens/month on Experiment tier."
        }
    },
    "free-muse-spark-api": {
        "title": "Free Muse Spark API — $0 Meta Model Endpoints & Limits (2026)",
        "h1": "Free Muse Spark API Endpoints & Rate Limits",
        "bluf": "Free Muse Spark API inference (Meta Muse Spark 1.3 Contributor Free with 1M context) is available on OpenRouter and OpenCode Zen with standard OpenAI-compatible base URLs.",
        "desc": "Free Muse Spark API directory. Rate limits, context windows, and base URLs for Meta Muse Spark 1.3 Contributor Free.",
        "filter": lambda p, m: "muse" in m["name"].lower() or "spark" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "meta/muse-spark-1.3-contributor:free",
            "provider": "OpenRouter",
            "notes": "Muse Spark 1.3 Contributor Free with 1M context window."
        }
    },
    "free-nemotron-api": {
        "title": "Free Nemotron API — NVIDIA Nemotron Endpoints & Limits (2026)",
        "h1": "Free Nemotron API Endpoints & Rate Limits",
        "bluf": "Free Nemotron API models—including Nemotron 3 Ultra 550B, 3.5 Lightning, and Super-VL—are available on OpenRouter (1M context), OpenCode Zen, and Requesty.",
        "desc": "Compare free NVIDIA Nemotron API providers. Verified rate limits and context windows for Nemotron 3 Ultra, Lightning, and Nano Omni.",
        "filter": lambda p, m: "nemotron" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "nvidia/nemotron-3.5-lightning:free",
            "provider": "OpenRouter",
            "notes": "NVIDIA Nemotron 3.5 Lightning with 1M context window."
        }
    },
    "free-gemma-api": {
        "title": "Free Gemma API — Google Gemma 4 Endpoints & Rate Limits (2026)",
        "h1": "Free Gemma API Endpoints & Rate Limits",
        "bluf": "Google Gemma 4 models (26B and 31B parameter models with 256K context) are accessible for free on SambaNova Cloud, OpenRouter, and Requesty with zero credit card required.",
        "desc": "Free Google Gemma API directory. Rate limits, context windows, and base URLs for Gemma 4 31B and 26B instruction-tuned models.",
        "filter": lambda p, m: "gemma" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://api.sambanova.ai/v1",
            "model": "gemma-4-31B-it",
            "provider": "SambaNova Cloud",
            "notes": "Google Gemma 4 31B parameter model via SambaNova."
        }
    },
    "free-cohere-api": {
        "title": "Free Cohere API — Command R+ & North Mini Endpoints (2026)",
        "h1": "Free Cohere API Endpoints & Rate Limits",
        "bluf": "Cohere provides a free trial key with 1,000 monthly calls across Command A and Command R+, while OpenRouter hosts cohere/north-mini-code:free with 250K context at $0.",
        "desc": "Free Cohere API key options. Rate limits and endpoints for Command R+, Command A, and North Mini Code models.",
        "filter": lambda p, m: "cohere" in m["name"].lower() or "cohere" in p["name"].lower(),
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "cohere/north-mini-code:free",
            "provider": "OpenRouter",
            "notes": "Cohere North Mini Code model hosted free on OpenRouter."
        }
    },
    "free-liquid-api": {
        "title": "Free Liquid API — LFM 2.5 Models & Rate Limits (2026)",
        "h1": "Free Liquid API Endpoints & Rate Limits",
        "bluf": "Liquid AI Liquid Foundation Models (LFM-2.5-2.6B with 64K context) are available completely free on OpenRouter at 20 RPM and up to 1,000 RPD.",
        "desc": "Free Liquid AI LFM API directory. Rate limits, context window, and base URLs for Liquid Foundation Models.",
        "filter": lambda p, m: "liquid" in m["name"].lower() or "lfm" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "liquid/lfm-2.5-2.6b:free",
            "provider": "OpenRouter",
            "notes": "Liquid AI LFM 2.5 2.6B model on OpenRouter."
        }
    },
    "free-poolside-api": {
        "title": "Free Poolside API — Laguna S & XS Models & Limits (2026)",
        "h1": "Free Poolside API Endpoints & Rate Limits",
        "bluf": "Poolside Laguna models (Laguna S 2.1 and XS 2.1 with 256K context) are available on OpenRouter free tier with 20 RPM and up to 1,000 RPD.",
        "desc": "Free Poolside API endpoints. Rate limits, context windows, and base URLs for Laguna S and Laguna XS code models.",
        "filter": lambda p, m: "poolside" in m["name"].lower() or "laguna" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "poolside/laguna-s-2.1:free",
            "provider": "OpenRouter",
            "notes": "Poolside Laguna S 2.1 model with 256K context."
        }
    },
    "free-inkling-api": {
        "title": "Free Inkling API — Thinking Machines Reasoning Models (2026)",
        "h1": "Free Inkling API Endpoints & Rate Limits",
        "bluf": "Thinking Machines Inkling and Inkling-Small reasoning models featuring 1M (1024K) context windows are hosted for free on OpenRouter with 20 RPM.",
        "desc": "Free Inkling reasoning API directory. Rate limits, 1M context windows, and base URLs for Thinking Machines models.",
        "filter": lambda p, m: "inkling" in m["name"].lower() or "thinkingmachines" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "thinkingmachines/inkling:free",
            "provider": "OpenRouter",
            "notes": "Thinking Machines Inkling reasoning model with 1024K context."
        }
    },
    "free-deepseek-v3-api": {
        "title": "Free DeepSeek-V3 API — $0 Endpoints & Rate Limits (2026)",
        "h1": "Free DeepSeek-V3 API Endpoints & Rate Limits",
        "bluf": "Free DeepSeek-V3.1 and V3.2 API access is live on SambaNova Cloud (128K context, high tok/s) and DeepInfra without requiring a paid subscription.",
        "desc": "Free DeepSeek-V3 API directory. Rate limits, context windows, and base URLs for DeepSeek-V3.1 and V3.2 without credit card.",
        "filter": lambda p, m: "deepseek" in m["name"].lower() and any(v in m["name"].lower() for v in ["v3", "3.1", "3.2"]),
        "tool_snippet": {
            "base_url": "https://api.sambanova.ai/v1",
            "model": "DeepSeek-V3.2",
            "provider": "SambaNova Cloud",
            "notes": "Direct OpenAI-compatible base URL for free DeepSeek-V3.2 inference."
        }
    },
    "free-qwen-coder-api": {
        "title": "Free Qwen Coder API — Coding Models & Rate Limits (2026)",
        "h1": "Free Qwen Coder API Endpoints & Rate Limits",
        "bluf": "Qwen 3.8 and Qwen 2.5 Coder models are available via Groq, Cerebras, DeepInfra, and AWS Kiro with standard OpenAI-compatible base URLs.",
        "desc": "Free Qwen Coder API directory. Compare rate limits, context windows, and providers offering free Qwen code generation models.",
        "filter": lambda p, m: "qwen" in m["name"].lower() and ("coder" in m["name"].lower() or "qwen" in m["name"].lower()),
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "qwen/qwen3.8-27b",
            "provider": "Groq",
            "notes": "Fast code generation with Qwen 3.8 on Groq."
        }
    },
    "free-llama-3-3-70b-api": {
        "title": "Free Llama 3.3 70B API — $0 Endpoints & Limits (2026)",
        "h1": "Free Llama 3.3 70B API Endpoints & Rate Limits",
        "bluf": "Meta Llama 3.3 70B Instruct is available with full free tier access on SambaNova Cloud (128K context) and Together AI ($5 trial credits) with OpenAI-compatible endpoints.",
        "desc": "Free Meta Llama 3.3 70B API endpoints. Verified rate limits, context windows, and setup guides without credit card.",
        "filter": lambda p, m: "llama" in m["name"].lower() and ("70b" in m["name"].lower() or "3.3" in m["name"].lower()),
        "tool_snippet": {
            "base_url": "https://api.sambanova.ai/v1",
            "model": "Meta-Llama-3.3-70B-Instruct",
            "provider": "SambaNova Cloud",
            "notes": "High-throughput Llama 3.3 70B Instruct via SambaNova Cloud."
        }
    },
    "free-gemini-flash-api": {
        "title": "Free Gemini Flash API — 1M Context & Rate Limits (2026)",
        "h1": "Free Gemini Flash API Endpoints & Rate Limits",
        "bluf": "Gemini 2.5 Flash, 3.5 Flash, and Flash-Lite provide 1,000,000 token context windows at 15 RPM completely free via Google AI Studio API and OpenAI base URL.",
        "desc": "Free Gemini Flash API directory. Compare rate limits, 1M context windows, and base URLs across all Gemini Flash versions.",
        "filter": lambda p, m: "gemini" in m["name"].lower() and "flash" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-2.5-flash",
            "provider": "Google AI Studio (Gemini API)",
            "notes": "Official Google AI Studio OpenAI-compatible endpoint with 1M context."
        }
    },
    "free-codestral-api": {
        "title": "Free Codestral API — Mistral Code Model & Limits (2026)",
        "h1": "Free Codestral API Endpoints & Rate Limits",
        "bluf": "Mistral Codestral is available for free developer use on Mistral La Plateforme Experiment tier at 1 req/sec and 1 billion tokens per month.",
        "desc": "Free Mistral Codestral API key setup. Rate limits, monthly token quotas, and base URLs for coding tasks.",
        "filter": lambda p, m: "codestral" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://api.mistral.ai/v1",
            "model": "Codestral",
            "provider": "Mistral La Plateforme",
            "notes": "Codestral endpoint with 1B free tokens/month on Experiment tier."
        }
    },
    "free-glm-4-flash-api": {
        "title": "Free GLM-4 Flash API — Fast $0 Endpoints & Limits (2026)",
        "h1": "Free GLM-4 Flash API Endpoints & Rate Limits",
        "bluf": "Z.AI provides GLM-4.7-Flash and GLM-4.5-Flash completely free with up to 203K context, fast inference speeds, and an OpenAI-compatible base URL.",
        "desc": "Free GLM-4 Flash API endpoints. Rate limits, context windows, and OpenAI-compatible base URL configuration for Z.AI.",
        "filter": lambda p, m: "glm-4" in m["name"].lower() and "flash" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://open.bigmodel.cn/api/paas/v4/",
            "model": "GLM-4.7-Flash",
            "provider": "Z.AI (Zhipu)",
            "notes": "OpenAI-compatible endpoint for free GLM-4.7-Flash inference."
        }
    },
    "free-llm-api": {
        "title": "Free LLM API Directory — All $0 Developer Endpoints (2026)",
        "h1": "Free LLM API Directory: Complete $0 Endpoints",
        "bluf": "Directory of all 18 LLM providers offering direct, free API keys for developers. Filtered by rate limits (RPM/TPM/RPD), context window size, and terms.",
        "desc": "Complete directory of free LLM APIs for developers. Compare rate limits, tokens per minute, daily caps, and context windows across all providers.",
        "filter": lambda p, m: p.get("access_method") == "api_key",
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "qwen/qwen3.8-27b",
            "provider": "Groq",
            "notes": "Direct, card-free LLM API key with sub-second response times."
        }
    },
    "free-llm-api-no-credit-card": {
        "title": "Free LLM API Without Credit Card — 14 Card-Free Providers (2026)",
        "h1": "Free LLM APIs Requiring No Credit Card",
        "bluf": "14 LLM providers offer permanently free API keys with zero credit card required at signup, including Google AI Studio, Groq, SambaNova, OpenRouter, and Z.AI.",
        "desc": "Verified free LLM APIs requiring no credit card at signup. Rate limits, context windows, and base URLs for 14 card-free inference providers.",
        "filter": lambda p, m: p.get("access_method") == "api_key" and "Trial" not in p.get("free_type", ""),
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "qwen/qwen3.8-27b",
            "provider": "Groq",
            "notes": "Card-free, instant developer key setup."
        }
    },
    "free-openai-compatible-api": {
        "title": "Free OpenAI-Compatible API — Base URLs & Drop-in Keys (2026)",
        "h1": "Free OpenAI-Compatible API Endpoints & Base URLs",
        "bluf": "17 free providers support the OpenAI /v1/chat/completions specification. Swap base_url and api_key directly in the OpenAI SDK, LangChain, LiteLLM, or Cursor.",
        "desc": "Free OpenAI-compatible API base URLs. Drop-in endpoints for Groq, SambaNova, Google AI Studio, DeepInfra, and Z.AI with code examples.",
        "filter": lambda p, m: bool(p.get("base_url")),
        "tool_snippet": {
            "base_url": "https://api.sambanova.ai/v1",
            "model": "DeepSeek-V3.2",
            "provider": "SambaNova Cloud",
            "notes": "Universal drop-in for any client expecting the OpenAI completions API."
        }
    },
    "free-keyless-api": {
        "title": "Free Keyless LLM API — Anonymous & Zero-Auth Endpoints (2026)",
        "h1": "Free Keyless LLM APIs: Zero Authentication Required",
        "bluf": "Keyless inference endpoints require no API key or account creation. Callable immediately via IP rate-limiting on OVHcloud, Kilo Gateway, and Hugging Face.",
        "desc": "Zero-auth and keyless LLM API endpoints. Test LLMs instantly without accounts, logins, or API keys using anonymous IP-limited endpoints.",
        "filter": lambda p, m: p.get("name") in ("OVHcloud AI Endpoints", "Kilo Gateway", "Cloudflare Workers AI", "Hugging Face"),
        "tool_snippet": {
            "base_url": "https://endpoints.ai.cloud.ovh.net/v1",
            "model": "Mistral 7B (Serverless)",
            "provider": "OVHcloud AI Endpoints",
            "notes": "Anonymous IP-based rate limiting without mandatory signup."
        }
    },
    "free-trial-credits": {
        "title": "Free LLM Trial Credits — $5 to $10 Free Developer Credits (2026)",
        "h1": "Free LLM API Trial Credits & Grants",
        "bluf": "High-throughput cloud providers offering free trial credits ($5-$10) for testing, including Cerebras (wafer-scale 2,000+ tok/s), DeepInfra, and Together AI.",
        "desc": "Free LLM trial credits and developer grants. Compare trial credit amounts, expiration terms, and throughput on Cerebras, DeepInfra, and Together AI.",
        "filter": lambda p, m: "Trial" in p.get("free_type", ""),
        "tool_snippet": {
            "base_url": "https://api.deepinfra.com/v1/openai",
            "model": "deepseek-ai/DeepSeek-V3.1",
            "provider": "DeepInfra",
            "notes": "Free sign-up trial credits with OpenAI-compatible API base URL."
        }
    },
    "free-coding-api": {
        "title": "Free Coding LLM API — Code Generation Models & Limits (2026)",
        "h1": "Free Coding LLM APIs & Code Generation Models",
        "bluf": "Free APIs specialized for code generation, refactoring, and agentic workflows, featuring Codestral, Qwen 3.8 Coder, North Mini Code, and Muse Spark Contributor.",
        "desc": "Best free coding LLM APIs. Rate limits, context windows, and base URLs for Codestral, Qwen Coder, and code-specialized models.",
        "filter": lambda p, m: any(w in m["name"].lower() for w in ["code", "coder", "codestral", "spark", "laguna"]) or (p.get("artifact") == "code" and p.get("access_method") == "api_key"),
        "tool_snippet": {
            "base_url": "https://api.mistral.ai/v1",
            "model": "Codestral",
            "provider": "Mistral La Plateforme",
            "notes": "Dedicated code generation model with 1B free tokens/month."
        }
    },
    "free-vision-api": {
        "title": "Free Vision LLM API — Multimodal Image & Text Models (2026)",
        "h1": "Free Vision & Multimodal LLM APIs",
        "bluf": "Free vision APIs supporting image understanding, OCR, and document analysis, including Gemini 2.5 Flash, GLM-4.6V-Flash, and Nemotron 3.5 Super-VL.",
        "desc": "Free vision LLM API directory. Rate limits and multimodal endpoints for Gemini Flash, GLM-4.6V, and Nemotron Super-VL.",
        "filter": lambda p, m: any(w in m["name"].lower() for w in ["vision", "vl", "omni", "flash-preview", "4.6v"]),
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-2.5-flash",
            "provider": "Google AI Studio (Gemini API)",
            "notes": "Multimodal image and video input via OpenAI-compatible endpoint."
        }
    },
    "free-reasoning-api": {
        "title": "Free Reasoning LLM API — Chain-of-Thought Models (2026)",
        "h1": "Free Reasoning & Chain-of-Thought LLM APIs",
        "bluf": "Free reasoning APIs offering extended thinking and step-by-step verification, featuring Nemotron Reasoning, Inkling, and DeepSeek R1 distills.",
        "desc": "Free reasoning and thinking LLM APIs. Rate limits, context windows, and base URLs for DeepSeek R1 distills and Nemotron reasoning models.",
        "filter": lambda p, m: any(w in m["name"].lower() for w in ["reasoning", "r1", "inkling", "ultra", "thinking"]),
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "thinkingmachines/inkling:free",
            "provider": "OpenRouter",
            "notes": "Chain-of-thought reasoning model with 1M context."
        }
    },
    "free-long-context-api": {
        "title": "Free Long-Context LLM API — 1M+ Token Windows at $0 (2026)",
        "h1": "Free Long-Context LLM APIs (128K to 1M+ Tokens)",
        "bluf": "Free LLM APIs supporting massive context windows from 128,000 to 1,000,000 tokens for large-codebase analysis and document synthesis.",
        "desc": "Directory of free long-context LLM APIs. Compare 128K, 256K, and 1,000,000 token context window providers and rate limits.",
        "filter": lambda p, m: any(w in str(m.get("context", "")).lower() for w in ["1000000", "1024k", "256k", "203k", "250k"]),
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-2.5-flash",
            "provider": "Google AI Studio (Gemini API)",
            "notes": "1,000,000 token context window on Google AI Studio free tier."
        }
    },
    "free-cursor-api": {
        "title": "Free API Keys for Cursor — OpenAI Base URLs & Setup (2026)",
        "h1": "Free API Keys for Cursor: OpenAI-Compatible Setup",
        "bluf": "Connect free high-speed LLM APIs directly to Cursor IDE using custom OpenAI Base URLs. Works with Groq, SambaNova, Google AI Studio, and DeepInfra with zero fees.",
        "desc": "How to get free API keys for Cursor IDE. Step-by-step OpenAI base URL override instructions, verified models, and speed benchmarks.",
        "filter": lambda p, m: bool(p.get("base_url")) and p.get("access_method") == "api_key",
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "qwen/qwen3.8-27b",
            "provider": "Groq",
            "notes": "In Cursor Settings → Models → OpenAI API Key → Override OpenAI Base URL, paste this URL."
        }
    },
    "free-cline-api": {
        "title": "Free API Keys for Cline & Roo Code — Endpoints & Setup (2026)",
        "h1": "Free API Endpoints for Cline & Roo Code",
        "bluf": "Configure Cline and Roo Code autonomous coding agents using free OpenAI-compatible endpoints or Google AI Studio keys without paying Anthropic or OpenAI API fees.",
        "desc": "Use free LLM APIs in Cline and Roo Code. Configure OpenAI-compatible providers, set custom base URLs, and choose optimal free coding models.",
        "filter": lambda p, m: bool(p.get("base_url")) and p.get("access_method") == "api_key",
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-2.5-flash",
            "provider": "Google AI Studio (Gemini API)",
            "notes": "In Cline settings, select OpenAI Compatible provider and enter this base URL."
        }
    },
    "free-claude-code-api": {
        "title": "Free API Keys for Claude Code — Compatible Providers (2026)",
        "h1": "Free API Keys & Endpoints for Claude Code CLI",
        "bluf": "Free endpoints compatible with Claude Code CLI and agent harnesses via OpenAI-compatible proxy layers, Google Gemini adapters, or Groq fast inference.",
        "desc": "How to run Claude Code CLI with free LLM endpoints. Compatible providers, proxy setup, and verified rate limits.",
        "filter": lambda p, m: bool(p.get("base_url")) and p.get("access_method") == "api_key",
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "qwen/qwen3.8-27b",
            "provider": "Groq",
            "notes": "Use with Claude Code CLI proxy wrappers or compatible agent frameworks."
        }
    }
}


def free_model_row_html(p, m):
    e = html.escape
    p_link = f'<a href="/providers/{slug(p["name"])}/">{e(p["name"])}</a>'
    cells = [
        f"<td><strong>{e(str(m['name']))}</strong></td>",
        f"<td>{p_link}</td>",
        f"<td>{e(str(m['cost']))}</td>",
        f"<td>{e(str(m['context']))}</td>",
        f"<td>{e(str(m['rpm']))}</td>",
        f"<td>{e(str(m['tpm']))}</td>",
        f"<td>{e(str(m['rpd']))}</td>",
        f"<td>{e(str(m['tpd']))}</td>",
        f"<td>{e(str(m['verified']))}</td>",
    ]
    return f"<tr>{''.join(cells)}</tr>"


def free_model_row_md(p, m):
    p_link = f"[{p['name']}](/providers/{slug(p['name'])}/)"
    vals = [m["name"], p_link, m["cost"], m["context"], m["rpm"], m["tpm"], m["rpd"], m["tpd"], m["verified"]]
    return "| " + " | ".join(str(v).replace("|", "\\|") for v in vals) + " |"


def free_answer_block(cfg, matched):
    bluf = cfg["bluf"]
    prov_count = len(set(p["name"] for p, _ in matched))
    model_count = len(matched)
    seen = set()
    top_provs = []
    for p, _ in matched:
        if p["name"] not in seen:
            seen.add(p["name"])
            top_provs.append(p)
            if len(top_provs) == 4:
                break
    takeaways = []
    for p in top_provs:
        p_models = [m["name"] for p_m, m in matched if p_m["name"] == p["name"]]
        models_str = ", ".join(p_models[:2])
        if len(p_models) > 2:
            models_str += f" (+{len(p_models)-2} more)"
        takeaways.append(f'<li><strong><a href="/providers/{slug(p["name"])}/">{html.escape(p["name"])}</a>:</strong> {html.escape(p["free_type"])} — {html.escape(models_str)}</li>')
    return f"""<section class="answer">
  <h2>Quick Answer</h2>
  <p>{html.escape(bluf)}</p>
  <ul>
    {"".join(takeaways)}
  </ul>
  <p class="answer-more">Total available in this directory: {count_noun(prov_count, 'provider')}, {count_noun(model_count, 'free model')}. Verified limits below.</p>
</section>"""


def free_footer_nav(verified):
    cols = []
    col_families = [
        ("free-deepseek-api", "Free DeepSeek API"),
        ("free-glm-api", "Free GLM API"),
        ("free-qwen-api", "Free Qwen API"),
        ("free-llama-api", "Free Llama API"),
        ("free-gemini-api", "Free Gemini API"),
        ("free-mistral-api", "Free Mistral API"),
        ("free-muse-spark-api", "Free Muse Spark API"),
        ("free-nemotron-api", "Free Nemotron API"),
        ("free-gemma-api", "Free Gemma API"),
        ("free-cohere-api", "Free Cohere API"),
    ]
    cols.append('<div class="fcol"><h3>Model Families</h3><ul>' +
                ''.join(f'<li><a href="/{s}/">{t}</a></li>' for s, t in col_families) +
                '</ul></div>')

    col_flagship = [
        ("free-deepseek-v3-api", "Free DeepSeek-V3 API"),
        ("free-qwen-coder-api", "Free Qwen Coder API"),
        ("free-llama-3-3-70b-api", "Free Llama 3.3 70B API"),
        ("free-gemini-flash-api", "Free Gemini Flash API"),
        ("free-codestral-api", "Free Codestral API"),
        ("free-glm-4-flash-api", "Free GLM-4 Flash API"),
        ("free-liquid-api", "Free Liquid LFM API"),
        ("free-poolside-api", "Free Poolside API"),
        ("free-inkling-api", "Free Inkling API"),
    ]
    cols.append('<div class="fcol"><h3>Flagship Models</h3><ul>' +
                ''.join(f'<li><a href="/{s}/">{t}</a></li>' for s, t in col_flagship) +
                '</ul></div>')

    col_friction = [
        ("free-llm-api", "Free LLM API Directory"),
        ("free-llm-api-no-credit-card", "No Credit Card APIs"),
        ("free-openai-compatible-api", "OpenAI Compatible APIs"),
        ("free-keyless-api", "Keyless / Anonymous APIs"),
        ("free-trial-credits", "Free Trial Credits ($5-$10)"),
    ]
    cols.append('<div class="fcol"><h3>Friction Tiers</h3><ul>' +
                ''.join(f'<li><a href="/{s}/">{t}</a></li>' for s, t in col_friction) +
                '</ul></div>')

    col_tools = [
        ("free-coding-api", "Free Coding APIs"),
        ("free-vision-api", "Free Vision APIs"),
        ("free-reasoning-api", "Free Reasoning APIs"),
        ("free-long-context-api", "Free Long Context APIs"),
        ("free-cursor-api", "Free Keys for Cursor"),
        ("free-cline-api", "Free Keys for Cline"),
        ("free-claude-code-api", "Free Keys for Claude Code"),
    ]
    cols.append('<div class="fcol"><h3>Tasks & Tools</h3><ul>' +
                ''.join(f'<li><a href="/{s}/">{t}</a></li>' for s, t in col_tools) +
                '</ul></div>')

    col_machine = [
        ("/", "Full Directory (Home)"),
        ("/llms.txt", "llms.txt (Agent Summary)"),
        ("/data/providers.json", "providers.json (Raw Data)"),
        ("/data/schema.json", "schema.json (JSON Schema)"),
        ("/sitemap.xml", "sitemap.xml (All Pages)"),
    ]
    cols.append('<div class="fcol"><h3>Machine & Catalog</h3><ul>' +
                ''.join(f'<li><a href="{u}">{t}</a></li>' for u, t in col_machine) +
                '</ul></div>')

    return ('<nav class="fcols" aria-label="Free API Slices">' + "".join(cols) + '</nav>'
            f'<p class="fnote">FreeInference.dev programmatic slice · verified {html.escape(verified)}. Limits change without notice — this is a map, not a contract.</p>')


def build_free_page(slug_key, cfg):
    matched = [(p, m) for p in ROWS for m in p["models"] if cfg["filter"](p, m)]
    title = cfg["title"]
    desc = cfg["desc"]
    h1 = cfg["h1"]
    page_url = f"{WEBSITE}/{slug_key}/"
    prov_count = len(set(p["name"] for p, _ in matched))
    model_count = len(matched)
    max_p = max_verified([p for p, _ in matched])
    verified = html.escape(max_p)
    verified_human = date.fromisoformat(max_p).strftime("%d %b %Y")
    tagline = f"{count_noun(prov_count, 'provider')} · {count_noun(model_count, 'free model')} · verified {verified_human}"
    answer = free_answer_block(cfg, matched)
    footer = free_footer_nav(verified)
    quick_connect_html = ""
    if "tool_snippet" in cfg:
        ts = cfg["tool_snippet"]
        b_url = html.escape(ts["base_url"])
        m_name = html.escape(ts["model"])
        p_name = html.escape(ts["provider"])
        p_slug = slug(ts["provider"])
        notes = html.escape(ts.get("notes", ""))
        quick_connect_html = f"""<section class="quick-connect">
  <h2>⚡ Quick Connect</h2>
  <p>{notes}</p>
  <div class="code-box"><code><strong>Base URL:</strong> {b_url}<br>
<strong>Model:</strong> {m_name}<br>
<strong>Provider:</strong> <a href="/providers/{p_slug}/">{p_name}</a></code></div>
  <pre class="code-box"><code class="language-python">from openai import OpenAI

client = OpenAI(
    base_url="{b_url}",
    api_key="your-api-key",  # from {p_name}
)

response = client.chat.completions.create(
    model="{m_name}",
    messages=[{{"role": "user", "content": "Hello!"}}],
)
print(response.choices[0].message.content)</code></pre>
</section>"""
    rows_html = "\n".join(free_model_row_html(p, m) for p, m in matched)
    ga_id = DATA.get("ga_measurement_id", "")
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>\n'
          f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}};'
          f"gtag('js',new Date());gtag('config','{ga_id}');</script>") if ga_id else ""
    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": title,
                "description": desc,
                "url": page_url,
                "dateModified": max_p,
                "version": DATA_VERSION,
                "isPartOf": {"@type": "Dataset", "name": TITLE, "url": WEBSITE},
                "isAccessibleForFree": True,
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "USD"
                }
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"How do I access {h1}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": cfg["bluf"]
                        }
                    }
                ]
            }
        ]
    }, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="data-version" content="{DATA_VERSION}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" type="text/markdown" href="{page_url}index.md">

<meta property="og:site_name" content="{html.escape(TITLE)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:updated_time" content="{verified}T00:00:00Z">

<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">

<link rel="icon" href="data:,">
{ga}
{PLAUSIBLE}\n{CLARITY}
<script type="application/ld+json">{ld}</script>
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{html.escape(h1)}</h1>
    <p class="tagline">{tagline}</p>
    <span class="meta"><a href="/">← all free providers</a> · <a href="/llms.txt">llms.txt</a></span>
  </header>

  {answer}

  {quick_connect_html}

  <section class="models">
    <h2>Rate Limits &amp; Model Inventory</h2>
    <div class="table-wrap"><table aria-label="{html.escape(h1)} rate limits and models">
      <thead><tr><th scope="col">Model</th><th scope="col">Provider</th><th scope="col">Cost</th><th scope="col">Context</th><th scope="col">RPM</th><th scope="col">TPM</th><th scope="col">RPD</th><th scope="col">Day tokens</th><th scope="col">Verified</th></tr></thead>
      <tbody>
{rows_html}
      </tbody>
    </table></div>
  </section>

  <p>Machine-readable: <a href="{page_url}index.md">Markdown Twin</a> · <a href="/data/providers.json">providers.json</a> · <a href="/sitemap.xml">sitemap.xml</a></p>
  <p><a href="/">← back to the full directory</a></p>

  <footer>
  {footer}
  </footer>
</div>
</body>
</html>
"""


def build_free_md(slug_key, cfg):
    matched = [(p, m) for p in ROWS for m in p["models"] if cfg["filter"](p, m)]
    h1 = cfg["h1"]
    bluf = cfg["bluf"]
    page_url = f"{WEBSITE}/{slug_key}/"
    prov_count = len(set(p["name"] for p, _ in matched))
    model_count = len(matched)
    max_p = max_verified([p for p, _ in matched])
    verified_human = date.fromisoformat(max_p).strftime("%d %b %Y")
    lines = [
        f"# {h1}",
        "",
        f"> {count_noun(prov_count, 'provider')} · {count_noun(model_count, 'free model')} · verified {verified_human}",
        "",
        "## Quick Answer",
        "",
        bluf,
        "",
    ]
    if "tool_snippet" in cfg:
        ts = cfg["tool_snippet"]
        lines += [
            "## Quick Connect",
            "",
            ts.get("notes", ""),
            "",
            f"- **Base URL:** `{ts['base_url']}`",
            f"- **Model:** `{ts['model']}`",
            f"- **Provider:** [{ts['provider']}](/providers/{slug(ts['provider'])}/)",
            "",
            "```python",
            "from openai import OpenAI",
            "",
            "client = OpenAI(",
            f"    base_url=\"{ts['base_url']}\",",
            f"    api_key=\"your-api-key\",  # from {ts['provider']}",
            ")",
            "",
            "response = client.chat.completions.create(",
            f"    model=\"{ts['model']}\",",
            "    messages=[{\"role\": \"user\", \"content\": \"Hello!\"}],",
            ")",
            "print(response.choices[0].message.content)",
            "```",
            "",
        ]
    lines += [
        "## Rate Limits & Model Inventory",
        "",
        "| Model | Provider | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for p, m in matched:
        lines.append(free_model_row_md(p, m))
    lines += [
        "",
        f"Web page: {page_url}",
        f"Machine-readable JSON: /data/providers.json",
        f"Agent summary: /llms.txt",
        "",
        f"Numbers cross-checked against official docs and live probes as of {max_p}. Limits change without notice — this is a map, not a contract.",
    ]
    return "\n".join(lines) + "\n"


def build_404():
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>404 — {html.escape(TITLE)}</title>
<meta name="robots" content="noindex">
<style>body{{font:16px/1.5 -apple-system,sans-serif;margin:0;display:grid;place-items:center;min-height:100vh;color:#1a1a1a}}a{{color:inherit}}</style></head>
<body><div><h1>404</h1><p>No such page. <a href="/">Back to the catalog.</a></p></div></body></html>
"""


def main():
    assert DATA["columns"] and ROWS, "empty columns or rows"
    required = {"name", "url", "free_type", "verified", "verified_method", "models"}
    model_required = {"name", "cost", "context", "rpm", "tpm", "rpd", "tpd", "verified"}
    for p in ROWS:
        missing = required - set(p)
        assert not missing, f"{p['name']}: missing {missing}"
        for m in p["models"]:
            missing_m = model_required - set(m)
            assert not missing_m, f"{p['name']}/{m.get('name', '?')}: missing {missing_m}"
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "data").mkdir(exist_ok=True)
    (ROOT / "README.md").write_text(build_readme())
    (dist / "index.html").write_text(build_html())
    (dist / "llms.txt").write_text(build_llms())
    (dist / "index.md").write_text(build_index_md())
    (dist / "404.html").write_text(build_404())
    for p in ROWS:
        pdir = dist / "providers" / slug(p["name"])
        pdir.mkdir(parents=True, exist_ok=True)
        (pdir / "index.html").write_text(build_provider_page(p))
        (pdir / "index.md").write_text(build_provider_md(p))
    for s, cfg in FREE_PAGES_CONFIG.items():
        sdir = dist / s
        sdir.mkdir(parents=True, exist_ok=True)
        (sdir / "index.html").write_text(build_free_page(s, cfg))
        (sdir / "index.md").write_text(build_free_md(s, cfg))
    sitemap_urls = [f"  <url><loc>{WEBSITE}/</loc><lastmod>{VERIFIED_MAX}</lastmod></url>"]
    sitemap_urls += [f"  <url><loc>{WEBSITE}/providers/{slug(p['name'])}/</loc><lastmod>{p['verified']}</lastmod></url>" for p in ROWS]
    sitemap_urls += [f"  <url><loc>{WEBSITE}/{s}/</loc><lastmod>{VERIFIED_MAX}</lastmod></url>" for s in sorted(FREE_PAGES_CONFIG.keys())]
    (dist / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(sitemap_urls) + "\n"
        "</urlset>\n"
    )
    out = dict(DATA)
    out["data_version"] = DATA_VERSION
    (dist / "data" / "providers.json").write_text(json.dumps(out, indent=2) + "\n")
    (dist / "data" / "schema.json").write_text(json.dumps(build_schema(), indent=2) + "\n")
    recent = sorted(
        ({"provider": p["name"], "verified": max_verified([p])} for p in ROWS),
        key=lambda x: x["verified"], reverse=True,
    )[:20]
    (dist / "data" / "changelog.json").write_text(json.dumps({
        "version": DATA_VERSION,
        "updated": VERIFIED_MAX,
        "providers": len(ROWS),
        "models": sum(len(p["models"]) for p in ROWS),
        "recent": recent,
    }, indent=2) + "\n")
    (dist / "_headers").write_text(
        f"/data/*\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"  Cache-Control: public, max-age=0, must-revalidate\n"
        f"/llms.txt\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"/index.md\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"/providers/*\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"/free-*\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
    )
    # ponytail: per-provider JSON split; whole file is ~40KB so single-file fetch stays the default path
    for p in ROWS:
        (dist / "data" / f"{slug(p['name'])}.json").write_text(json.dumps(p, indent=2) + "\n")
    ai_bots = ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
               "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot", "Amazonbot")
    (dist / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n"
        + "".join(f"User-agent: {b}\nAllow: /\n" for b in ai_bots)
        + f"# LLMs: {WEBSITE}/llms.txt\n"
        + f"Sitemap: {WEBSITE}/sitemap.xml\n"
    )
    (dist / "b4d83ac2bcee40a798bc63319e92d730.txt").write_text("b4d83ac2bcee40a798bc63319e92d730")
    total = sum(len(p["models"]) for p in ROWS)
    index_html = (dist / "index.html").read_text()
    assert index_html.count('href="/providers/') >= len(ROWS), "footer provider links missing"
    assert "FreeInference" in index_html, "brand missing from homepage title"
    assert f'name="data-version" content="{DATA_VERSION}"' in index_html, "data version missing"
    titles = []
    for p in ROWS:
        page = (dist / "providers" / slug(p["name"]) / "index.html").read_text()
        m = re.search(r"<title>(.*?)</title>", page)
        assert m, f"{p['name']}: missing title"
        assert len(m.group(1)) <= 75, f"{p['name']}: title too long ({len(m.group(1))})"
        assert f'name="data-version" content="{DATA_VERSION}"' in page, f"{p['name']}: data version missing"
        titles.append(m.group(1))
    assert len(titles) == len(set(titles)), "duplicate provider titles"
    free_titles = []
    for s, cfg in FREE_PAGES_CONFIG.items():
        page = (dist / s / "index.html").read_text()
        m = re.search(r"<title>(.*?)</title>", page)
        assert m, f"{s}: missing title"
        assert len(m.group(1)) <= 75, f"{s}: title too long ({len(m.group(1))})"
        assert f'name="data-version" content="{DATA_VERSION}"' in page, f"{s}: data version missing"
        assert f'<link rel="canonical" href="{WEBSITE}/{s}/">' in page, f"{s}: canonical URL missing"
        assert f'<link rel="alternate" type="text/markdown" href="{WEBSITE}/{s}/index.md">' in page, f"{s}: md alternate missing"
        free_titles.append(m.group(1))
    assert len(free_titles) == len(set(free_titles)), "duplicate free page titles"
    print(f"ok: {count_noun(len(ROWS), 'provider')}, {count_noun(total, 'model')} -> dist/ (verified {VERIFIED_MAX}, version {DATA_VERSION})")
    print(f"verify: {len(titles)} provider pages · {len(free_titles)} free-* pages · {index_html.count('href=\"/providers/')} footer links")


if __name__ == "__main__":
    main()