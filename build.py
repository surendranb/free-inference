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
import struct
import zlib
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

TURNSTILE_SITE_KEY = "0x4AAAAAAF4X6Cad5QW5V0Bs"

TURNSTILE_SCRIPT = """<!-- Cloudflare Turnstile -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>"""


def gtag():
    # ponytail: one gtag snippet for every page; empty when ga_measurement_id unset
    ga_id = DATA.get("ga_measurement_id", "")
    if not ga_id:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>\n'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}};'
            f"gtag('js',new Date());gtag('config','{ga_id}');</script>")


FAVICON_TAGS = """<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="alternate icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/atom+xml" title="Free Inference Changelog Feed" href="/feed.xml">"""

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

### Quick Navigation & Machine Access

- 🤖 **Agent Skill (`SKILL.md`)**: [{WEBSITE}/skill.md]({WEBSITE}/skill.md) (install: `curl -fsSL {WEBSITE}/skill.md -o ~/.agents/skills/free-inference/SKILL.md`)
- 📋 **OpenAI Catalog Endpoint**: `GET {WEBSITE}/v1/models`
- 📡 **Changelog RSS/Atom Feed**: [{WEBSITE}/feed.xml]({WEBSITE}/feed.xml)
- 📬 **Weekly Dispatch (Newsletter)**: [{WEBSITE}/newsletter/]({WEBSITE}/newsletter/)
- 💳 **No Credit Card or Subscription**: [{WEBSITE}/free-llm-api-no-credit-card/]({WEBSITE}/free-llm-api-no-credit-card/)
- ⚡ **OpenAI-Compatible Drop-in Endpoints**: [{WEBSITE}/free-openai-compatible-api/]({WEBSITE}/free-openai-compatible-api/)
- 🛠 **Free Coding & Cursor / Cline Keys**: [{WEBSITE}/free-coding-api/]({WEBSITE}/free-coding-api/) · [{WEBSITE}/free-cursor-api/]({WEBSITE}/free-cursor-api/)
- 🧠 **Top Model Guides**: [DeepSeek V3.2]({WEBSITE}/free-deepseek-api/) · [Llama 3.3 70B]({WEBSITE}/free-llama-api/) · [Qwen 3.8]({WEBSITE}/free-qwen-api/) · [Gemini 3.5 Flash-Lite]({WEBSITE}/free-gemini-api/) · [GLM-5 / 4.7]({WEBSITE}/free-glm-api/)

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
                        "channel": {"type": "string", "enum": ["api", "feed", "web"]},
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



NEWSLETTER_FORM_SNIPPET = f"""<form class="newsletter-form" onsubmit="event.preventDefault();var f=this,b=f.querySelector('button'),i=f.querySelector('input[type=email]'),hp=f.querySelector('input[name=b_name]'),m=f.querySelector('.newsletter-msg');var token='';if(typeof turnstile!=='undefined'){{try{{token=turnstile.getResponse()||'';}}catch(e){{}}}}if(!token){{var ti=f.querySelector('[name=cf-turnstile-response]');if(ti)token=ti.value||'';}}if(!token){{m.textContent='Please complete the security check.';m.style.color='#991b1b';return;}}b.disabled=true;b.textContent='Subscribing...';fetch('/api/subscribe',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{email:i.value,turnstileToken:token,b_name:hp?hp.value:''}})}}).then(function(r){{return r.json()}}).then(function(d){{if(d.success){{b.textContent='Subscribed!';i.disabled=true;m.textContent='You are on the list. Issues drop Mondays at 09:00 IST.';m.style.color='#166534';}}else{{b.disabled=false;b.textContent='Subscribe';m.textContent=d.error||'Failed to subscribe';m.style.color='#991b1b';if(typeof turnstile!=='undefined'){{try{{turnstile.reset()}}catch(e){{}}}}}}}}).catch(function(){{b.disabled=false;b.textContent='Subscribe';m.textContent='Network error. Please try again.';m.style.color='#991b1b';}});"><div style="position:absolute;left:-9999px;opacity:0;pointer-events:none;" aria-hidden="true"><input type="text" name="b_name" tabindex="-1" autocomplete="off"></div><div class="newsletter-form-row"><input type="email" name="email" placeholder="you@domain.com" required aria-label="Your email address"><button type="submit">Subscribe</button></div><div class="cf-turnstile" data-sitekey="{TURNSTILE_SITE_KEY}" data-theme="light" data-size="flexible" style="margin-top:6px;"></div><div class="newsletter-msg"></div></form>"""


FOOTER_PROVIDER_GROUPS = [
    ("AI Labs & Clouds", [
        "google-ai-studio--gemini-api", "mistral-la-plateforme", "nvidia-nim--build-nvidia-com",
        "cohere", "sambanova-cloud", "cloudflare-workers-ai", "deepseek-platform",
        "z-ai--zhipu", "liquid-ai", "dots-studio", "braintrust",
    ]),
    ("Inference Gateways", [
        "openrouter", "groq", "cerebras", "deepinfra", "opencode-zen",
        "siliconflow", "requesty", "kilo-gateway", "nous-portal", "ovhcloud-ai-endpoints",
    ]),
    ("Coding Agents & IDEs", [
        "github-copilot--free", "cursor--hobby", "windsurf", "devin--free", "kiro--aws",
        "trae--bytedance", "bolt-new", "lovable", "v0--vercel", "replit--starter", "qoder",
    ]),
    ("Audio, Sandboxes & Builders", [
        "deepgram", "assemblyai", "google-colab", "kaggle-notebooks",
        "hugging-face-spaces", "antigravity-cli--google", "figma--starter", "canva--free", "framer--free",
    ]),
]

FOOTER_CAPABILITY_GROUPS = [
    ("Tasks & Modalities", [
        ("free-coding-api", "Coding & Code Gen"),
        ("free-audio-api", "Audio & Voice APIs"),
        ("free-stt-api", "Speech-to-Text (STT)"),
        ("free-tts-api", "Text-to-Speech (TTS)"),
        ("free-whisper-api", "Hosted Whisper Models"),
        ("free-vision-api", "Vision & Multimodal"),
        ("free-reasoning-api", "Reasoning & Chain-of-Thought"),
        ("free-long-context-api", "Long Context (128K–1M)"),
    ]),
    ("Access & Setup", [
        ("free-inference-providers", "AI Inference Providers"),
        ("free-inference-api", "Free Inference APIs"),
        ("free-llm-api", "Complete $0 Directory"),
        ("free-llm-api-no-credit-card", "No Credit Card Required"),
        ("free-openai-compatible-api", "OpenAI-Compatible Base URLs"),
        ("free-keyless-api", "Keyless / Anonymous APIs"),
        ("free-trial-credits", "Free Trial Credits ($5–$200)"),
        ("free-cursor-api", "Free Keys for Cursor"),
        ("free-cline-api", "Free Endpoints for Cline"),
        ("free-claude-code-api", "Free Keys for Claude Code"),
    ]),
    ("Flagship Models", [
        ("free-deepseek-v3-api", "DeepSeek-V3"),
        ("free-qwen-coder-api", "Qwen 2.5 Coder"),
        ("free-llama-3-3-70b-api", "Llama 3.3 70B"),
        ("free-gemini-flash-api", "Gemini Flash"),
        ("free-codestral-api", "Mistral Codestral"),
        ("free-glm-4-flash-api", "GLM-4 Flash"),
        ("free-liquid-api", "Liquid LFM"),
        ("free-poolside-api", "Poolside"),
        ("free-inkling-api", "Inkling"),
    ]),
    ("Model Families", [
        ("free-deepseek-api", "DeepSeek (V3/R1)"),
        ("free-llama-api", "Meta Llama"),
        ("free-qwen-api", "Alibaba Qwen"),
        ("free-gemini-api", "Google Gemini"),
        ("free-mistral-api", "Mistral AI"),
        ("free-gemma-api", "Google Gemma"),
        ("free-glm-api", "Zhipu GLM"),
        ("free-nemotron-api", "NVIDIA Nemotron"),
        ("free-cohere-api", "Cohere Command"),
        ("free-muse-spark-api", "Muse Spark"),
    ]),
]

# Backwards compatibility alias
FOOTER_GROUPS = FOOTER_PROVIDER_GROUPS


def footer_nav(verified, include_newsletter=True):
    by_slug = {slug(p["name"]): p for p in ROWS}
    total_models = sum(len(p["models"]) for p in ROWS)

    # 1. Capability Taxonomy (35 slices across 4 columns)
    cap_cols = []
    for label, items in FOOTER_CAPABILITY_GROUPS:
        li_items = "".join(f'<li><a href="/{s}/">{html.escape(title)}</a></li>' for s, title in items)
        cap_cols.append(f'<div class="fcol"><h3>{html.escape(label)}</h3><ul>{li_items}</ul></div>')

    # 2. Complete Provider Taxonomy (41 providers across 4 columns)
    grouped = set()
    prov_cols = []
    for label, slugs in FOOTER_PROVIDER_GROUPS:
        items = []
        for s in slugs:
            p = by_slug.get(s)
            if p:
                grouped.add(s)
                items.append(f'<li><a href="/providers/{s}/">{html.escape(p["name"])}</a></li>')
        if items:
            prov_cols.append(f'<div class="fcol"><h3>{html.escape(label)}</h3><ul>{"".join(items)}</ul></div>')

    # Dynamic fallback: if future providers are added without taxonomy updates, list under Newly Added
    leftovers = [s for s in by_slug if s not in grouped]
    if leftovers:
        items = "".join(f'<li><a href="/providers/{s}/">{html.escape(by_slug[s]["name"])}</a></li>' for s in leftovers)
        prov_cols.append(f'<div class="fcol"><h3>Newly Added</h3><ul>{items}</ul></div>')

    newsletter_html = f"""<section class="newsletter-box">
  <h3>⚡ Free Inference Weekly</h3>
  <p>Curated $0 LLM quotas, newly verified models, and breaking changes drafted every Monday by the Antigravity Agent. Zero spam, unsubscribe in 1 click.</p>
  {NEWSLETTER_FORM_SNIPPET}
</section>""" if include_newsletter else ""

    return f"""{newsletter_html}
<div class="fsection">
  <div class="fheader">
    <h2>Directory by Capability</h2>
    <p>Browse verified $0 inference by modality, access requirement, and model family.</p>
  </div>
  <nav class="fgrid" aria-label="Directory by Capability">
    {"".join(cap_cols)}
  </nav>
</div>

<div class="fsection">
  <div class="fheader">
    <h2>All Verified Providers ({len(ROWS)})</h2>
    <p>Direct access methods: API keys, IDE bundles, and cloud developer sandboxes.</p>
  </div>
  <nav class="fgrid" aria-label="All Verified Providers">
    {"".join(prov_cols)}
  </nav>
</div>

<div class="fbottom">
  <div class="fbottom-links">
    <span class="fbottom-title">Machine & Agent Interfaces:</span>
    <a href="/v1/models">OpenAI API (/v1/models)</a> ·
    <a href="/skill.md">Antigravity Skill (skill.md)</a> ·
    <a href="/llms.txt">Agent Context (llms.txt)</a> ·
    <a href="/data/providers.json">JSON Dataset</a> ·
    <a href="/data/schema.json">JSON Schema</a> ·
    <a href="/feed.xml">RSS Feed</a> ·
    <a href="/newsletter/">Weekly Dispatch</a> ·
    <a href="/index.md">Raw Markdown</a> ·
    <a href="/sitemap.xml">Sitemap</a>
  </div>
  <p class="fmeta">{count_noun(len(ROWS), "provider")} · {count_noun(total_models, "free model")} · verified {html.escape(verified)}. Limits change without notice — this is an autonomous map, not a contract.</p>
</div>"""


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
                 f"or inference bundled in an IDE. No credit card required. Last updated: {VERIFIED_HUMAN}.")
    og_desc = (f"{count_noun(total_models, 'free LLM model')} across {count_noun(provider_count, 'provider')} (including Google AI Studio, Groq, "
               f"OpenRouter, and OpenCode Zen). OpenAI-compatible endpoints, rate limits, and context windows. Last updated: {VERIFIED_HUMAN}.")

    head_title = html.escape(page_title)
    head_meta = html.escape(meta_desc)
    head_og = html.escape(og_desc)
    data_json = json.dumps(DATA, ensure_ascii=False, indent=1)
    logos_json = json.dumps({p["name"]: logo_file(slug(p["name"])) for p in ROWS}, ensure_ascii=False)
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
    ga = gtag()

    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": TITLE,
        "description": og_desc,
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
<meta name="description" content="{head_meta}">
<meta name="data-version" content="{DATA_VERSION}">
<link rel="canonical" href="{website}">
<link rel="alternate" type="text/markdown" href="{website}/index.md">
<link rel="alternate" type="text/plain" title="LLM summary" href="{website}/llms.txt">

<!-- OpenGraph / Social Metadata -->
<meta property="og:site_name" content="{html.escape(TITLE)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{website}">
<meta property="og:title" content="{head_title}">
<meta property="og:description" content="{head_og}">
<meta property="og:updated_time" content="{verified}T00:00:00Z">

<!-- Twitter / X Metadata -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{head_title}">
<meta name="twitter:description" content="{head_og}">

{FAVICON_TAGS}
{ga}
{PLAUSIBLE}
{CLARITY}
{TURNSTILE_SCRIPT}
<script type="application/ld+json">{ld}</script>
<link rel="stylesheet" href="/style.css">
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
const LOGOS = {logos_json};
const DEFS = {json.dumps(definitions(), ensure_ascii=False)};
</script>
<script defer src="/app.js"></script>
</body>
</html>
"""


def row_html(p):
    name = html.escape(p["name"])
    tds = "".join(f"<td>{html.escape(str(cell(p, c)))}</td>" for c in COLS[1:])
    return f'<tr><td><a href="{html.escape(p["url"])}" target="_blank" rel="noopener">{name}</a></td>{tds}</tr>'


def slug(name):
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


LOGO_DIR = ROOT / "data" / "logos"


def logo_file(s):
    # ponytail: disk truth beats naming convention — logos are stored as {slug}.svg or {slug}--{variant}.svg
    if (LOGO_DIR / f"{s}.svg").exists():
        return f"{s}.svg"
    variant = sorted(LOGO_DIR.glob(f"{s}--*.svg"))
    return variant[0].name if variant else f"{s}.svg"


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
    ga = gtag()
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

{FAVICON_TAGS}
{PLAUSIBLE}
{CLARITY}
{ga}
{TURNSTILE_SCRIPT}
<script type="application/ld+json">{ld}</script>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="wrap">
  <header>
    <div class="provider-title-row">
      <img src="/logos/{logo_file(s)}" class="provider-logo" alt="{name} logo" width="36" height="36" onerror="this.style.display='none'">
      <h1>{name}</h1>
    </div>
    <p class="tagline">{free_type} · {access_label} · {artifact} · Last updated: {verified_human}</p>
    <span class="meta"><a href="/">← directory</a> · <a href="/v1/models">/v1/models</a> · <a href="{REPO}">github</a></span>
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
        "bluf": "Google AI Studio provides 16 free models (including Gemini 3.5 Flash-Lite and 3.1 Flash-Lite at 500 RPD, plus Gemma 4 open-weight models at 14.4K RPD) with 1M context windows and an official OpenAI-compatible endpoint.",
        "desc": "Complete reference for Google AI Studio free Gemini API tier. Verified RPM, TPM, RPD, and 1M context limits across all Gemini models.",
        "filter": lambda p, m: "gemini" in m["name"].lower() or "google ai studio" in p["name"].lower(),
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-3.5-flash-lite",
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
        "bluf": "Thinking Machines Inkling models are currently unlisted on free tiers after OpenRouter ended its free promotional window. Verified alternative reasoning models with 128K–1M context windows include DeepSeek-R1 and Nemotron Reasoning.",
        "desc": "Free Inkling reasoning API directory. Upstream status, alternative reasoning models, rate limits, and 1M context endpoints.",
        "filter": lambda p, m: "inkling" in m["name"].lower() or "thinkingmachines" in m["name"].lower(),
        "fallback_filter": lambda p, m: any(k in m["name"].lower() for k in ["nemotron-3-nano-omni", "deepseek-r1", "gemini-3.5-flash-lite"]),
        "upstream_notice": "Thinking Machines Inkling and Inkling-Small models have rotated off OpenRouter's free promotional tier and are currently paid-only upstream ($1.00/$4.05 per 1M tokens). The table below lists active, verified $0 alternative reasoning models with long context windows.",
        "tool_snippet": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
            "provider": "OpenRouter",
            "notes": "Verified free reasoning alternative on OpenRouter with 128K context and 20 RPM."
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
        "bluf": "Gemini 3.5 Flash-Lite, 3.1 Flash-Lite, and 3.5 Flash provide 1,000,000 token context windows at 15 RPM completely free via Google AI Studio API and OpenAI base URL.",
        "desc": "Free Gemini Flash API directory. Compare rate limits, 1M context windows, and base URLs across all Gemini Flash versions.",
        "filter": lambda p, m: "gemini" in m["name"].lower() and "flash" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-3.5-flash-lite",
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
    "free-inference-providers": {
        "title": "Free AI Inference Providers — $0 Host Comparison (2026)",
        "h1": "Free AI & LLM Inference Providers",
        "bluf": "Directory comparing verified zero-cost AI inference providers, hardware accelerators, and API gateways. Filtered by rate limits, token throughput, and context windows.",
        "desc": "Compare free AI and LLM inference providers. Verified rate limits, context windows, and base URLs for SambaNova, Groq, Cerebras, Google AI Studio, and DeepInfra.",
        "filter": lambda p, m: p.get("access_method") == "api_key",
        "tool_snippet": {
            "base_url": "https://api.sambanova.ai/v1",
            "model": "DeepSeek-V3.2",
            "provider": "SambaNova Cloud",
            "notes": "Ultra-fast zero-cost inference provider with 131K context window."
        }
    },
    "free-inference-api": {
        "title": "Free Inference API — $0 OpenAI-Compatible Endpoints (2026)",
        "h1": "Free Inference APIs & Endpoints",
        "bluf": "Verified free inference APIs supporting OpenAI-compatible chat completions. Direct developer keys with zero credit card required, sub-second latency, and drop-in SDK base URLs.",
        "desc": "Directory of verified free inference APIs. Drop-in OpenAI-compatible endpoints, rate limits, and cURL examples for Groq, SambaNova, Google AI Studio, and Cerebras.",
        "filter": lambda p, m: bool(p.get("base_url")) and p.get("access_method") == "api_key",
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "llama-3.3-70b-versatile",
            "provider": "Groq",
            "notes": "Drop-in OpenAI-compatible inference API with ultra-low latency LPU throughput."
        }
    },
    "free-llm-api": {
        "title": "Free LLM API Directory — All $0 Developer Endpoints (2026)",
        "h1": "Free LLM API Directory: Complete $0 Endpoints",
        "bluf": "Directory of verified LLM providers offering direct, free API keys for developers with zero subscription. Filtered by rate limits (RPM/TPM/RPD), context window size, and terms.",
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
        "title": "Free LLM API Without Credit Card — No Subscription Required (2026)",
        "h1": "Free LLM APIs Requiring No Credit Card or Subscription",
        "bluf": "Verified LLM providers offering permanently free API keys with zero credit card and no paid subscription required at signup, including Google AI Studio, Groq, SambaNova, OpenRouter, and Z.AI.",
        "desc": "Verified free LLM APIs requiring no credit card or subscription at signup. Rate limits, context windows, and base URLs for 14 card-free inference providers.",
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
        "bluf": "Free vision APIs supporting image understanding, OCR, and document analysis, including Gemini 3.5 Flash-Lite, GLM-4.6V-Flash, and Nemotron 3.5 Super-VL.",
        "desc": "Free vision LLM API directory. Rate limits and multimodal endpoints for Gemini Flash, GLM-4.6V, and Nemotron Super-VL.",
        "filter": lambda p, m: any(w in m["name"].lower() for w in ["vision", "vl", "omni", "flash-preview", "4.6v"]),
        "tool_snippet": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-3.5-flash-lite",
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
            "model": "gemini-3.5-flash-lite",
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
            "model": "gemini-3.5-flash-lite",
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
    },
    "free-stt-api": {
        "title": "Free Speech-to-Text API — $0 Audio Transcription (2026)",
        "h1": "Free Speech-to-Text (STT) APIs & Audio Transcription",
        "bluf": "Free speech-to-text API endpoints for audio transcription, including Groq (Whisper Large v3 at 2,000 requests/day), Deepgram ($200 credits), and AssemblyAI ($50 credits) with zero credit card required.",
        "desc": "Free speech-to-text API directory. Compare rate limits, audio size limits, and base URLs for Whisper, Nova-3, and Universal-1 without paid subscriptions.",
        "filter": lambda p, m: any(w in m["name"].lower() for w in ["whisper", "nova", "universal", "conformer", "stt"]) or "audio" in m.get("context", "").lower() or "speech-to-text" in m.get("context", "").lower(),
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "whisper-large-v3-turbo",
            "provider": "Groq",
            "notes": "Hosted Whisper Large v3 Turbo on Groq LPU with 2,000 requests/day free."
        }
    },
    "free-tts-api": {
        "title": "Free Text-to-Speech API — $0 Voice Synthesis (2026)",
        "h1": "Free Text-to-Speech (TTS) APIs & Voice Synthesis",
        "bluf": "Free text-to-speech API endpoints for voice synthesis and voice agents, including Groq (CanopyLabs Orpheus) and Deepgram (Aura) with generous free allowances and no credit card required.",
        "desc": "Free text-to-speech API directory. Compare rate limits, audio quotas, and endpoints for Orpheus and Aura voice synthesis.",
        "filter": lambda p, m: any(w in m["name"].lower() for w in ["orpheus", "aura", "tts"]) or "text-to-speech" in m.get("context", "").lower(),
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "canopylabs/orpheus-v1-english",
            "provider": "Groq",
            "notes": "Text-to-speech audio synthesis with Orpheus on Groq."
        }
    },
    "free-whisper-api": {
        "title": "Free Whisper API — $0 Hosted OpenAI Whisper Endpoints (2026)",
        "h1": "Free Hosted Whisper API Endpoints & Rate Limits",
        "bluf": "Free hosted OpenAI Whisper API endpoints for high-throughput speech transcription, including Groq (Whisper Large v3 & Turbo at 2,000 RPD) and Cloudflare Workers AI with zero credit card.",
        "desc": "Free hosted Whisper API endpoints. Compare audio limits, time-to-first-token, and request quotas for Whisper Large v3 on Groq and Cloudflare.",
        "filter": lambda p, m: "whisper" in m["name"].lower(),
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "whisper-large-v3-turbo",
            "provider": "Groq",
            "notes": "Fastest hosted Whisper Large v3 Turbo transcription endpoint."
        }
    },
    "free-audio-api": {
        "title": "Free Audio AI API — $0 Speech-to-Text & Voice Synthesis (2026)",
        "h1": "Free Audio & Voice Inference APIs",
        "bluf": "Complete directory of verified free audio inference APIs covering Speech-to-Text (STT) and Text-to-Speech (TTS) across Groq, Deepgram, AssemblyAI, and Cloudflare Workers AI.",
        "desc": "Directory of free audio AI APIs. Compare free quotas, audio minutes, and endpoints for Whisper, Orpheus, Nova, and Aura.",
        "filter": lambda p, m: any(w in m["name"].lower() for w in ["whisper", "orpheus", "nova", "aura", "universal", "conformer", "stt", "tts", "audio"]) or "audio" in m.get("context", "").lower() or "text-to-speech" in m.get("context", "").lower(),
        "tool_snippet": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "whisper-large-v3-turbo",
            "provider": "Groq",
            "notes": "Unified audio speech recognition and synthesis."
        }
    }
}


def free_model_row_html(p, m):
    e = html.escape
    pslug = slug(p["name"])
    p_link = f'<a href="/providers/{pslug}/" class="prov-link"><img src="/logos/{logo_file(pslug)}" class="prow-logo" width="16" height="16" alt="" onerror="this.style.display=\'none\'"> {e(p["name"])}</a>'
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
    return footer_nav(verified, include_newsletter=True)


def generate_slice_descriptions(cfg, matched, verified_human):
    prov_count = len(set(p["name"] for p, _ in matched))
    model_count = len(matched)

    top_p = []
    for p, _ in matched:
        p_name = p["name"].split(" (")[0]
        if p_name not in top_p:
            top_p.append(p_name)
            if len(top_p) == 3:
                break

    topic = cfg["h1"]
    for prefix in ["Free ", "Zero-Cost "]:
        if topic.startswith(prefix):
            topic = topic[len(prefix):]
    for suffix in [" Endpoints & Rate Limits", " Models", " Free Tier", " Models & Inference"]:
        if topic.endswith(suffix):
            topic = topic[:-len(suffix)]

    top_two = ", ".join(top_p[:2])
    p_noun = count_noun(prov_count, "provider")

    # Surface 1: SEO Meta Description (Target: 140-160 chars)
    meta_desc = f"{model_count} free {topic} models across {p_noun} ({top_two}). $0 endpoints, rate limits & keys. Last updated: {verified_human}."

    # Surface 2: Social & Agent OG Description (Target: 200-260 chars)
    provs_og = ", ".join(top_p[:-1]) + f", and {top_p[-1]}" if len(top_p) > 2 else " and ".join(top_p)
    og_desc = f"{model_count} free {topic} models across {p_noun} including {provs_og}. Verified rate limits, context windows, and OpenAI-compatible endpoints. Last updated: {verified_human}."

    return meta_desc, og_desc


def build_free_page(slug_key, cfg):
    matched = [(p, m) for p in ROWS for m in p["models"] if cfg["filter"](p, m)]
    is_fallback = False
    if not matched:
        is_fallback = True
        fb_fn = cfg.get("fallback_filter")
        if fb_fn:
            matched = [(p, m) for p in ROWS for m in p["models"] if fb_fn(p, m)]
        if not matched:
            matched = [(p, m) for p in ROWS for m in p["models"] if any(k in m["name"].lower() for k in ["reasoning", "r1", "flash", "nemotron"])][:5]

    title = cfg["title"]
    h1 = cfg["h1"]
    page_url = f"{WEBSITE}/{slug_key}/"
    prov_count = len(set(p["name"] for p, _ in matched))
    model_count = len(matched)
    max_p = max_verified([p for p, _ in matched])
    verified = html.escape(max_p)
    verified_human = date.fromisoformat(max_p).strftime("%d %b %Y")
    meta_desc, og_desc = generate_slice_descriptions(cfg, matched, verified_human)
    tagline_status = " (recommended alternatives)" if is_fallback else ""
    tagline = f"{count_noun(prov_count, 'provider')} · {count_noun(model_count, 'free model')}{tagline_status} · Last updated: {verified_human}"
    answer = free_answer_block(cfg, matched)
    footer = free_footer_nav(verified)
    notice_html = ""
    if is_fallback:
        custom_notice = cfg.get("upstream_notice", "Models for this category are currently unlisted or paid-only on upstream provider free tiers. The table below lists verified active $0 alternative models.")
        notice_html = f"""<aside class="upstream-notice" style="background:#fff3cd;border:1px solid #ffeeba;border-left:4px solid #ffc107;padding:12px 16px;margin:16px 0;border-radius:4px;">
  <p style="margin:0;color:#856404;font-size:14px;line-height:1.5;"><strong>⚠️ Upstream Status Notice:</strong> {html.escape(custom_notice)}</p>
</aside>"""
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
  <p><strong>Python (OpenAI SDK):</strong></p>
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
  <p><strong>cURL (Terminal / Shell):</strong></p>
  <pre class="code-box"><code class="language-bash">curl -X POST "{b_url}/chat/completions" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer $API_KEY" \\
  -d '{{
    "model": "{m_name}",
    "messages": [{{"role": "user", "content": "Hello!"}}]
  }}'</code></pre>
</section>"""
    rows_html = "\n".join(free_model_row_html(p, m) for p, m in matched)
    ga = gtag()
    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": title,
                "description": og_desc,
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

{FAVICON_TAGS}
{ga}
{PLAUSIBLE}
{CLARITY}
{TURNSTILE_SCRIPT}
<script type="application/ld+json">{ld}</script>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="wrap">
  <header>
    <h1>{html.escape(h1)}</h1>
    <p class="tagline">{tagline}</p>
    <span class="meta"><a href="/">← directory</a> · <a href="/v1/models">/v1/models</a> · <a href="{REPO}">github</a></span>
  </header>

  {answer}

  {notice_html}

  {quick_connect_html}

  <section class="models">
    <h2>{'Rate Limits &amp; Recommended Free Alternatives' if is_fallback else 'Rate Limits &amp; Model Inventory'}</h2>
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
    is_fallback = False
    if not matched:
        is_fallback = True
        fb_fn = cfg.get("fallback_filter")
        if fb_fn:
            matched = [(p, m) for p in ROWS for m in p["models"] if fb_fn(p, m)]
        if not matched:
            matched = [(p, m) for p in ROWS for m in p["models"] if any(k in m["name"].lower() for k in ["reasoning", "r1", "flash", "nemotron"])][:5]

    h1 = cfg["h1"]
    bluf = cfg["bluf"]
    page_url = f"{WEBSITE}/{slug_key}/"
    prov_count = len(set(p["name"] for p, _ in matched))
    model_count = len(matched)
    max_p = max_verified([p for p, _ in matched])
    verified_human = date.fromisoformat(max_p).strftime("%d %b %Y")
    meta_desc, og_desc = generate_slice_descriptions(cfg, matched, verified_human)
    tagline_status = " (recommended alternatives)" if is_fallback else ""
    lines = [
        f"# {h1}",
        "",
        f"> {count_noun(prov_count, 'provider')} · {count_noun(model_count, 'free model')}{tagline_status} · Last updated: {verified_human}",
        "",
    ]
    if is_fallback:
        custom_notice = cfg.get("upstream_notice", "Models for this category are currently unlisted or paid-only on upstream provider free tiers. The table below lists verified active $0 alternative models.")
        lines += [
            f"> ⚠️ **Upstream Status Notice:** {custom_notice}",
            "",
        ]
    lines += [
        "## Quick Answer",
        "",
        og_desc,
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
            "### Python (OpenAI SDK)",
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
            "### cURL (Terminal / Shell)",
            "",
            "```bash",
            f"curl -X POST \"{ts['base_url']}/chat/completions\" \\",
            "  -H \"Content-Type: application/json\" \\",
            "  -H \"Authorization: Bearer $API_KEY\" \\",
            "  -d '{",
            f"    \"model\": \"{ts['model']}\",",
            "    \"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}]",
            "  }'",
            "```",
            "",
        ]
    lines += [
        "## Rate Limits & Recommended Free Alternatives" if is_fallback else "## Rate Limits & Model Inventory",
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


def copy_static_assets(dist):
    import shutil
    src_dir = ROOT / "data" / "logos"
    if src_dir.exists():
        dst_dir = dist / "logos"
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in src_dir.glob("*.svg"):
            shutil.copy2(f, dst_dir / f.name)
    static_dir = ROOT / "static"
    if static_dir.exists():
        for f in static_dir.glob("*"):
            if f.is_file():
                shutil.copy2(f, dist / f.name)


def build_favicon(dist):
    # Happy Hues #17: Navy #001858, Teal #8bd3dd, Pink #f582ae
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect width="32" height="32" rx="6" fill="#001858"/>
  <path d="M17 4 L9 17 L15 17 L13 28 L23 14 L17 14 Z" fill="url(#bolt-grad)"/>
  <defs>
    <linearGradient id="bolt-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8bd3dd"/>
      <stop offset="100%" stop-color="#f582ae"/>
    </linearGradient>
  </defs>
</svg>
"""
    (dist / "favicon.svg").write_text(svg_content)

    def create_rgba(size):
        raw = bytearray()
        r_corner = size * 0.2
        scale = size / 32.0
        poly = [
            (17 * scale, 4 * scale),
            (9 * scale, 17 * scale),
            (15 * scale, 17 * scale),
            (13 * scale, 28 * scale),
            (23 * scale, 14 * scale),
            (17 * scale, 14 * scale),
        ]

        def point_in_poly(x, y, p):
            inside = False
            n = len(p)
            p1x, p1y = p[0]
            for i in range(n + 1):
                p2x, p2y = p[i % n]
                if y > min(p1y, p2y):
                    if y <= max(p1y, p2y):
                        if x <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1y = p2x, p2y
            return inside

        for y in range(size):
            raw.append(0)  # filter type none
            for x in range(size):
                cx = min(max(x, r_corner), size - 1 - r_corner)
                cy = min(max(y, r_corner), size - 1 - r_corner)
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if d > r_corner:
                    raw.extend([0, 0, 0, 0])
                else:
                    if point_in_poly(x + 0.5, y + 0.5, poly):
                        if y < size * 0.55:
                            raw.extend([139, 211, 221, 255])  # teal #8bd3dd
                        else:
                            raw.extend([245, 130, 174, 255])  # pink #f582ae
                    else:
                        raw.extend([0, 24, 88, 255])  # navy #001858
        return bytes(raw)

    def encode_png(width, height, raw_bytes):
        def chunk(tag, data):
            return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
        idat = zlib.compress(raw_bytes, 9)
        return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")

    def encode_ico(png_data, width=32, height=32):
        header = struct.pack("<HHH", 0, 1, 1)
        entry = struct.pack(
            "<BBBBHHII",
            width if width < 256 else 0,
            height if height < 256 else 0,
            0,
            0,
            1,
            32,
            len(png_data),
            22,
        )
        return header + entry + png_data

    png32 = encode_png(32, 32, create_rgba(32))
    png180 = encode_png(180, 180, create_rgba(180))
    ico32 = encode_ico(png32, 32, 32)

    (dist / "apple-touch-icon.png").write_bytes(png180)
    (dist / "favicon.ico").write_bytes(ico32)


def build_v1_endpoints(dist):
    v1_dir = dist / "v1"
    v1_dir.mkdir(parents=True, exist_ok=True)
    (dist / "models").parent.mkdir(parents=True, exist_ok=True)

    model_entries = []
    for p in ROWS:
        for m in p["models"]:
            model_entries.append({
                "id": m["name"],
                "object": "model",
                "created": 1730000000,
                "owned_by": p["name"],
                "permission": [],
                "root": m["name"],
                "parent": None,
                "free_tier": {
                    "provider": p["name"],
                    "provider_url": p["url"],
                    "base_url": p.get("base_url") or "",
                    "access_method": p.get("access_method") or "",
                    "free_type": p["free_type"],
                    "cost": m["cost"],
                    "context": m["context"],
                    "rpm": m["rpm"],
                    "tpm": m["tpm"],
                    "rpd": m["rpd"],
                    "tpd": m["tpd"],
                    "verified": m["verified"],
                },
            })

    models_payload = {
        "object": "list",
        "data": model_entries,
        "last_updated": VERIFIED_MAX,
        "data_version": DATA_VERSION,
        "total_models": len(model_entries),
    }

    models_json_str = json.dumps(models_payload, indent=2) + "\n"
    (v1_dir / "models").write_text(models_json_str)
    (dist / "models").write_text(models_json_str)

    chat_notice = {
        "error": {
            "message": "FreeInference.dev is an open verified catalog and directory of $0 free inference providers, not an API proxy or inference gateway. Direct inference requests (POST /v1/chat/completions) are not executed on this domain. To run free inference, query our catalog at /v1/models to select a provider, and route your requests directly to that provider's base_url (e.g. Groq, SambaNova, Google AI Studio, Cerebras).",
            "type": "catalog_only_directory",
            "param": None,
            "code": "method_not_allowed",
        },
        "catalog": {
            "directory_url": WEBSITE,
            "models_endpoint": f"{WEBSITE}/v1/models",
            "raw_json": f"{WEBSITE}/data/providers.json",
            "llms_txt": f"{WEBSITE}/llms.txt",
            "documentation": f"{WEBSITE}/free-openai-compatible-api/",
        },
        "skill": {
            "name": "free-inference",
            "description": "Official Agent Skill for Cursor, Claude Code, Cline, and LLM agent loops to automatically query, filter, and configure verified $0 endpoints and rate limits.",
            "install_url": f"{WEBSITE}/skill.md",
            "canonical_url": f"{WEBSITE}/skills/free-inference/SKILL.md",
            "instructions": f"Download or reference {WEBSITE}/skill.md in your agent prompt to dynamically discover active free models.",
        },
        "newsletter": {
            "name": "FreeInference Weekly Dispatch",
            "description": "Weekly automated email digest tracking new free models, quota changes, and verified $0 provider drops.",
            "web_archive": f"{WEBSITE}/newsletter/",
            "api_subscribe": {
                "endpoint": f"{WEBSITE}/api/subscribe",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": {"email": "developer@example.com"},
                "curl_example": f"curl -X POST {WEBSITE}/api/subscribe -H 'Content-Type: application/json' -d '{{\"email\": \"you@example.com\"}}'",
            },
        },
        "feed": {
            "atom_feed": f"{WEBSITE}/feed.xml",
            "description": "Atom / RSS syndication feed for automated catalog aggregators, RSS readers, and agent monitors.",
        },
        "quick_drop_in_providers": [
            {
                "provider": "SambaNova Cloud",
                "base_url": "https://api.sambanova.ai/v1",
                "recommended_model": "DeepSeek-V3.2",
                "free_tier": "Free API key, 0 credit card, 131k context window",
                "signup_url": "https://cloud.sambanova.ai",
            },
            {
                "provider": "Groq",
                "base_url": "https://api.groq.com/openai/v1",
                "recommended_model": "llama-3.3-70b-versatile",
                "free_tier": "Free API key, 0 credit card, ultra-low latency LPU",
                "signup_url": "https://console.groq.com",
            },
            {
                "provider": "Google AI Studio",
                "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
                "recommended_model": "gemini-3.5-flash-lite",
                "free_tier": "15 RPM, 500 RPD permanently free, 1,000,000 token context window",
                "signup_url": "https://aistudio.google.com",
            },
            {
                "provider": "Cerebras",
                "base_url": "https://api.cerebras.ai/v1",
                "recommended_model": "llama-3.3-70b",
                "free_tier": "Free trial credits, 2,000+ tokens/sec throughput",
                "signup_url": "https://cloud.cerebras.ai",
            },
        ],
    }
    (v1_dir / "chat").mkdir(parents=True, exist_ok=True)
    (v1_dir / "chat" / "completions").write_text(json.dumps(chat_notice, indent=2) + "\n")


def build_skill(dist):
    skills_dir = ROOT / "skills" / "free-inference"
    skills_dir.mkdir(parents=True, exist_ok=True)
    dist_skills_dir = dist / "skills" / "free-inference"
    dist_skills_dir.mkdir(parents=True, exist_ok=True)

    total_models = sum(len(p["models"]) for p in ROWS)
    total_provs = len(ROWS)

    skill_content = f"""---
name: free-inference
description: Query, filter, and configure verified $0 free LLM inference providers, OpenAI-compatible base URLs, and active rate limits (RPM/TPM/RPD) across {total_provs} providers and {total_models} models.
version: 1.0.0
updated: {VERIFIED_MAX}
homepage: {WEBSITE}
update_url: {WEBSITE}/skills/free-inference/SKILL.md
short_url: {WEBSITE}/skill.md
models_url: {WEBSITE}/v1/models
---

# Free Inference Agent Skill

> **⚡ Live Freshness & Update Protocol**:
> Free tier quotas, models, and endpoints change without notice. Before recommending any endpoint, or to update your local skill heuristics to the latest catalog state, fetch:
> **`{WEBSITE}/skills/free-inference/SKILL.md`** (or short URL **`{WEBSITE}/skill.md`**)
>
> Real-time machine models catalog: **`{WEBSITE}/v1/models`** · Raw JSON: **`{WEBSITE}/data/providers.json`**

Use this skill when the user asks for free LLM APIs, $0 inference endpoints, drop-in keys for coding tools (Cursor, Cline, Claude Code, Aider), rate limits, or context windows.

---

## 1. Quick Task Heuristics

When the user specifies a task, prioritize these verified $0 providers:

### A. Coding Assistants (Cursor, Cline, Claude Code, Aider)
- **Groq**: Ultra-low latency via LPU.
  - Base URL: `https://api.groq.com/openai/v1`
  - Top Models: `llama-3.3-70b-versatile`, `qwen/qwen3.6-27b`, `meta-llama/llama-4-scout-17b-16e-instruct`
  - Access: Free API key, no credit card required.
- **SambaNova Cloud**: High throughput, full frontier open models.
  - Base URL: `https://api.sambanova.ai/v1`
  - Top Models: `DeepSeek-V3.2`, `Meta-Llama-3.3-70B-Instruct`
  - Access: Free API key, no credit card, universal OpenAI drop-in.
- **OpenCode Zen**: Generous developer limits.
  - Base URL: `https://opencode.ai/inference/openai/v1`
  - Top Models: `Big Pickle`, `GLM-5.3-Flash Free`, `DeepSeek V4.1 Flash Free`
  - Access: Free developer key.

### B. Massive Context Windows (>= 128k - 1M Tokens)
- **Google AI Studio (Gemini API)**: 1,000,000 token context window.
  - Base URL: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - Top Models: `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemma-4-26b-a4b-it`, `gemma-4-31b-it`
  - Access: 15–30 RPM, 500–14.4K RPD, $0 permanently, no credit card.
- **OpenCode Zen**: Up to 1M context on `Big Pickle`.
- **SambaNova Cloud**: 131k context on `DeepSeek-V3.2`.

### C. Drop-in OpenAI Compatibility (`base_url` swap)
To use any free provider in code expecting OpenAI's client, swap `base_url` and `api_key`:
- SambaNova: `https://api.sambanova.ai/v1`
- Groq: `https://api.groq.com/openai/v1`
- Google AI Studio: `https://generativelanguage.googleapis.com/v1beta/openai/`
- DeepInfra: `https://api.deepinfra.com/v1/openai`
- Z.AI (Zhipu): `https://open.bigmodel.cn/api/paas/v4/`

### D. Zero Credit Card Required (Permanently $0)
Google AI Studio, Groq, SambaNova Cloud, OpenRouter, Cloudflare Workers AI, DeepInfra, Z.AI, Hugging Face, Cerebras (trial).

---

## 2. Real-Time Verification Step

Before generating an implementation for a user, check live availability against the FreeInference endpoint:

```bash
# Query all models live
curl -s {WEBSITE}/v1/models | jq '.data[] | select(.id | test("DeepSeek|Llama|Qwen"; "i")) | {{id, provider: .free_tier.provider, base_url: .free_tier.base_url, rpm: .free_tier.rpm}}'
```

Or in Python:
```python
import urllib.request, json

req = urllib.request.Request("{WEBSITE}/v1/models", headers={{"User-Agent": "FreeInference-Agent/1.0"}})
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)
    print(f"Catalog contains {{data['total_models']}} free models across {{len(data['data'])}} entries.")
```

---

## 3. Drop-in Python Example

```python
from openai import OpenAI

# Example: SambaNova Cloud ($0 DeepSeek-V3.2)
client = OpenAI(
    base_url="https://api.sambanova.ai/v1",
    api_key="your-sambanova-key",
)

response = client.chat.completions.create(
    model="DeepSeek-V3.2",
    messages=[{{"role": "user", "content": "Write a fast binary search in Python."}}],
)
print(response.choices[0].message.content)
```

---

## 4. Updates & Ground Truth
- Full interactive directory: [{WEBSITE}]({WEBSITE})
- Complete Markdown Twin: [{WEBSITE}/index.md]({WEBSITE}/index.md)
- Agent Summary: [{WEBSITE}/llms.txt]({WEBSITE}/llms.txt)
- Atom/RSS Feed: [{WEBSITE}/feed.xml]({WEBSITE}/feed.xml)
- Update this skill: `curl -fsSL {WEBSITE}/skill.md -o ~/.agents/skills/free-inference/SKILL.md`
"""

    (skills_dir / "SKILL.md").write_text(skill_content)
    (dist_skills_dir / "SKILL.md").write_text(skill_content)
    (dist / "skill.md").write_text(skill_content)


def build_feed(dist):
    entries = []
    sorted_provs = sorted(ROWS, key=lambda p: max_verified([p]), reverse=True)[:15]

    for p in sorted_provs:
        p_verified = max_verified([p])
        p_slug = slug(p["name"])
        models_str = html.escape(", ".join(m["name"] for m in p["models"][:5]))
        if len(p["models"]) > 5:
            models_str += f", +{len(p['models']) - 5} more"
        notes = html.escape(p.get("notes", "Verified free inference tier."))

        entry_xml = f"""  <entry>
    <title>{html.escape(p['name'])}: {html.escape(p['free_type'])} ({len(p['models'])} free models)</title>
    <link href="{WEBSITE}/providers/{p_slug}/"/>
    <id>urn:freeinference:provider:{p_slug}:{p_verified}</id>
    <updated>{p_verified}T00:00:00Z</updated>
    <summary type="html"><![CDATA[
      <p><strong>Provider:</strong> {html.escape(p['name'])}</p>
      <p><strong>Free Tier:</strong> {html.escape(p['free_type'])}</p>
      <p><strong>Models:</strong> {models_str}</p>
      <p><strong>Notes:</strong> {notes}</p>
      <p><a href="{WEBSITE}/providers/{p_slug}/">View limits and base URLs</a></p>
    ]]></summary>
    <author><name>FreeInference.dev</name></author>
  </entry>"""
        entries.append(entry_xml)

    feed_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{html.escape(TITLE)} Updates</title>
  <subtitle>{html.escape(TAGLINE)}</subtitle>
  <link href="{WEBSITE}/feed.xml" rel="self"/>
  <link href="{WEBSITE}/"/>
  <updated>{VERIFIED_MAX}T00:00:00Z</updated>
  <id>{WEBSITE}/</id>
  <author><name>FreeInference.dev</name></author>
{chr(10).join(entries)}
</feed>
"""
    (dist / "feed.xml").write_text(feed_xml)


def build_newsletter_page(dist):
    ndir = dist / "newsletter"
    ndir.mkdir(parents=True, exist_ok=True)
    newsletters_dir = ROOT / "data" / "newsletters"
    newsletters_dir.mkdir(parents=True, exist_ok=True)

    issues = []
    for f in sorted(newsletters_dir.glob("*.md"), reverse=True):
        content = f.read_text()
        first_line = content.splitlines()[0] if content.splitlines() else f.stem
        title = first_line.lstrip("#").strip()
        issues.append((f.stem, title, content))

    issues_html = ""
    if issues:
        issues_html = "<h2>Recent Dispatches</h2>\n<ul class=\"dispatch-list\">\n"
        for stem, title, content in issues:
            issues_html += f"""  <li>
    <h3>{html.escape(title)}</h3>
    <p class=\"dmeta\">Published {html.escape(stem)} · Drafted by Antigravity Agent</p>
    <div class=\"code-box\"><pre>{html.escape(content)}</pre></div>
  </li>\n"""
        issues_html += "</ul>\n"
    else:
        issues_html = "<p>No dispatches published yet. The inaugural issue drops this Monday at 09:00 IST.</p>"

    html_content = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Free Inference Dispatch — Weekly $0 AI Inference Updates</title>
<meta name="description" content="Weekly developer dispatch covering verified $0 LLM quotas, newly cataloged models, and rate limit changes drafted by the Antigravity Agent.">
<meta name="data-version" content="{DATA_VERSION}">
<link rel="canonical" href="{WEBSITE}/newsletter/">
{FAVICON_TAGS}
{PLAUSIBLE}
{CLARITY}
{TURNSTILE_SCRIPT}
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="wrap">
  <header>
    <h1>The Free Inference Dispatch</h1>
    <p class="tagline">Weekly $0 LLM quotas, newly cataloged models, and breaking changes drafted every Monday by the Antigravity Agent.</p>
    <span class="meta"><a href="/">← directory</a> · <a href="/v1/models">/v1/models</a> · <a href="/skill.md">skill.md</a> · <a href="{REPO}">github</a></span>
  </header>

  <section class="newsletter-box" style="margin-top:0;">
    <h3>⚡ Subscribe to The Weekly Dispatch</h3>
    <p>Get the weekly diff delivered to your inbox every Monday at 09:00 IST. Strictly verified $0 endpoints, zero marketing hype, unsubscribe in 1 click.</p>
    {NEWSLETTER_FORM_SNIPPET}
  </section>

  <p>Also available via machine feeds: <a href="/feed.xml">RSS / Atom Feed (feed.xml)</a> · <a href="/skill.md">Agent Skill (skill.md)</a> · <a href="/v1/models">OpenAI Catalog API (/v1/models)</a></p>

  {issues_html}

  <p><a href="/">← back to the full directory</a></p>
</div>
</body>
</html>
"""
    (ndir / "index.html").write_text(html_content)


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
    build_favicon(dist)
    copy_static_assets(dist)
    build_v1_endpoints(dist)
    build_skill(dist)
    build_feed(dist)
    build_newsletter_page(dist)
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
    sitemap_urls = [
        f"  <url><loc>{WEBSITE}/</loc><lastmod>{VERIFIED_MAX}</lastmod></url>",
        f"  <url><loc>{WEBSITE}/newsletter/</loc><lastmod>{VERIFIED_MAX}</lastmod></url>",
        f"  <url><loc>{WEBSITE}/skill.md</loc><lastmod>{VERIFIED_MAX}</lastmod></url>",
        f"  <url><loc>{WEBSITE}/feed.xml</loc><lastmod>{VERIFIED_MAX}</lastmod></url>",
    ]
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
        f"/v1/*\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Access-Control-Allow-Methods: GET, POST, OPTIONS\n"
        f"  Access-Control-Allow-Headers: *\n"
        f"  Content-Type: application/json; charset=utf-8\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"/models\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Access-Control-Allow-Methods: GET, OPTIONS\n"
        f"  Access-Control-Allow-Headers: *\n"
        f"  Content-Type: application/json; charset=utf-8\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"/skill.md\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Content-Type: text/markdown; charset=utf-8\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"  Cache-Control: public, max-age=3600\n"
        f"/skills/*\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Content-Type: text/markdown; charset=utf-8\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"  Cache-Control: public, max-age=3600\n"
        f"/style.css\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Content-Type: text/css; charset=utf-8\n"
        f"  Cache-Control: public, max-age=86400\n"
        f"/app.js\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Content-Type: application/javascript; charset=utf-8\n"
        f"  Cache-Control: public, max-age=86400\n"
        f"/logos/*\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Content-Type: image/svg+xml; charset=utf-8\n"
        f"  Cache-Control: public, max-age=86400\n"
        f"/feed.xml\n"
        f"  Access-Control-Allow-Origin: *\n"
        f"  Content-Type: application/atom+xml; charset=utf-8\n"
        f"  X-Data-Version: {DATA_VERSION}\n"
        f"  X-Last-Verified: {VERIFIED_MAX}\n"
        f"  Cache-Control: public, max-age=3600\n"
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
        f"/favicon.*\n"
        f"  Cache-Control: public, max-age=604800, immutable\n"
        f"/apple-touch-icon.png\n"
        f"  Cache-Control: public, max-age=604800, immutable\n"
    )
    (dist / "_redirects").write_text(
        "/v1/models/ /v1/models 301\n"
        "/models/ /models 301\n"
        "/skill /skill.md 301\n"
        "/skills/free-inference /skills/free-inference/SKILL.md 301\n"
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
    assert (dist / "style.css").stat().st_size > 0, "missing dist/style.css"
    assert (dist / "app.js").stat().st_size > 0, "missing dist/app.js"
    assert (dist / "favicon.ico").stat().st_size > 0, "missing favicon.ico"
    assert (dist / "favicon.svg").stat().st_size > 0, "missing favicon.svg"
    assert (dist / "apple-touch-icon.png").stat().st_size > 0, "missing apple-touch-icon.png"
    assert (dist / "v1" / "models").stat().st_size > 0, "missing /v1/models"
    assert (dist / "models").stat().st_size > 0, "missing /models"
    assert (dist / "v1" / "chat" / "completions").stat().st_size > 0, "missing /v1/chat/completions"
    assert (dist / "skill.md").stat().st_size > 0, "missing dist/skill.md"
    assert (dist / "skills" / "free-inference" / "SKILL.md").stat().st_size > 0, "missing SKILL.md"
    assert (dist / "feed.xml").stat().st_size > 0, "missing dist/feed.xml"
    assert (dist / "newsletter" / "index.html").stat().st_size > 0, "missing newsletter page"
    index_html = (dist / "index.html").read_text()
    assert '<link rel="stylesheet" href="/style.css">' in index_html, "missing style.css in index.html"
    assert '<script defer src="/app.js"></script>' in index_html, "missing app.js in index.html"
    assert index_html.count('href="/providers/') >= len(ROWS), "footer provider links missing"
    assert "FreeInference" in index_html, "brand missing from homepage title"
    assert f'name="data-version" content="{DATA_VERSION}"' in index_html, "data version missing"
    logos = json.loads(re.search(r"const LOGOS = (\{.*?\});", index_html).group(1))
    assert len(logos) == len(ROWS), "logo map incomplete"
    assert all((dist / "logos" / f).exists() for f in logos.values()), "index logo 404"
    titles = []
    for p in ROWS:
        page = (dist / "providers" / slug(p["name"]) / "index.html").read_text()
        m = re.search(r"<title>(.*?)</title>", page)
        assert m, f"{p['name']}: missing title"
        assert len(m.group(1)) <= 75, f"{p['name']}: title too long ({len(m.group(1))})"
        assert f'name="data-version" content="{DATA_VERSION}"' in page, f"{p['name']}: data version missing"
        assert "googletagmanager" in page, f"{p['name']}: GA4 tag missing"
        assert '<link rel="stylesheet" href="/style.css">' in page, f"{p['name']}: missing style.css"
        names = re.findall(r'/logos/([^"\s]+\.svg)', page)
        assert names and all((dist / "logos" / n).exists() for n in names), f"{p['name']}: logo 404 ({names})"
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
        assert '<link rel="stylesheet" href="/style.css">' in page, f"{s}: missing style.css"
        names = re.findall(r'/logos/([^"\s]+\.svg)', page)
        assert names and all((dist / "logos" / n).exists() for n in names), f"{s}: logo 404 ({names})"
        free_titles.append(m.group(1))
    assert len(free_titles) == len(set(free_titles)), "duplicate free page titles"
    print(f"ok: {count_noun(len(ROWS), 'provider')}, {count_noun(total, 'model')} -> dist/ (verified {VERIFIED_MAX}, version {DATA_VERSION})")
    print(f"verify: {len(titles)} provider pages · {len(free_titles)} free-* pages · {index_html.count('href=\"/providers/')} footer links")


if __name__ == "__main__":
    main()