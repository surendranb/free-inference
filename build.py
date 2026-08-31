#!/usr/bin/env python3
"""Build Free Inference site artifacts from data/providers.json (single source of truth).

Outputs into dist/ (gitignored; deployed by Cloudflare Pages on push):
  dist/index.html           — two-pane catalog (sidebar providers | models panel), no-JS fallback
  dist/llms.txt             — agent-readable summary (llmstxt.org)
  dist/data/providers.json  — machine data
  dist/data/schema.json     — JSON Schema for providers.json (agents validate before trusting)
  dist/robots.txt           — allow all crawlers
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data" / "providers.json").read_text())

COLS = DATA["columns"]
ROWS = DATA["providers"]
VERIFIED = DATA["verified"]
TITLE = DATA["title"]
TAGLINE = DATA["tagline"]
WEBSITE = DATA.get("website", "")
REPO = DATA.get("repo", "")

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

> **{VERIFIED}** · {len(ROWS)} providers · {total} free models
> Interactive site: {WEBSITE} · Agent summary: {WEBSITE}/llms.txt · Machine data: {WEBSITE}/data/providers.json (validate against {WEBSITE}/data/schema.json)

## Providers

| Provider | Free tier | Notable models | Notes |
| --- | --- | --- | --- |
"""
    prov_rows = []
    for p in ROWS:
        name = f"[{p['name']}]({p['url']})"
        models = ", ".join(m["name"] for m in p["models"][:6])
        if len(p["models"]) > 6:
            models += f", +{len(p['models']) - 6} more"
        prov_rows.append(f"| {name} | {p['free_type']} | {models} | {p.get('notes', '—')} |")
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
        f"Last verified: {VERIFIED} · {len(ROWS)} providers · {total_models} free models.",
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
        lines.append(f"- [{p['name']}]({p['url']}): {p['free_type']} · {p['verified_method']} · verified {p['verified']} · models: {models}")
        for m in p["models"]:
            lines.append(
                f"  - {m['name']}: cost {m['cost']} · context {m['context']} · "
                f"RPM {m['rpm']} · TPM {m['tpm']} · RPD {m['rpd']} · day tokens {m['tpd']} · verified {m['verified']}"
            )
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


def build_html():
    total_models = sum(len(p["models"]) for p in ROWS)
    provider_count = len(ROWS)
    sample_providers = ", ".join(p["name"] for p in ROWS[:5])

    page_title = f"{TITLE} — {total_models} Free LLM Models Across {provider_count} Providers (Updated {VERIFIED})"
    meta_desc = (f"Updated {VERIFIED} · {provider_count} providers & {total_models} verified free models "
                 f"({sample_providers}, etc.). Verified rate limits (RPM, TPM, RPD), "
                 f"context windows, and browser WebMCP tools for AI agents and harnesses.")

    head_title = html.escape(page_title)
    head_desc = html.escape(meta_desc)
    data_json = json.dumps(DATA, ensure_ascii=False, indent=1)
    verified = html.escape(VERIFIED)
    website = html.escape(WEBSITE)
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
        "dateModified": VERIFIED,
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
<link rel="canonical" href="{website}">
<link rel="alternate" type="text/markdown" href="{website}/index.md">

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
<script type="application/ld+json">{ld}</script>
<style>
  :root {{ --bg:#fff; --ink:#1a1a1a; --mut:#6b6b6b; --line:#e3e3e3; --sel:#111; --selink:#fff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  a {{ color:var(--ink); }}
  .wrap {{ max-width:1500px; margin:0 auto; padding:32px 24px 64px; }}
  header {{ display:flex; align-items:baseline; gap:16px; border-bottom:1px solid var(--line);
           padding-bottom:16px; margin-bottom:20px; }}
  h1 {{ font-size:24px; margin:0; letter-spacing:-.01em; }}
  .tagline {{ color:var(--mut); margin:0; max-width:800px; font-size:15px; }}
  .meta {{ color:var(--mut); font-size:13px; margin-left:auto; white-space:nowrap; }}
  .layout {{ display:grid; grid-template-columns:280px 1fr; gap:20px; align-items:start; }}
  @media (max-width:860px) {{ .layout {{ grid-template-columns:1fr; }} .meta {{ display:none; }} }}
  .sidebar {{ border:1px solid var(--line); border-radius:8px; overflow:hidden;
              position:sticky; top:16px; background:var(--bg); }}
  @media (max-width:860px) {{ .sidebar {{ position:static; }} }}
  #filter {{ width:100%; border:none; border-bottom:1px solid var(--line); padding:10px 14px;
            font:inherit; font-size:14px; outline:none; background:var(--bg); }}
  #providers {{ max-height:74vh; overflow-y:auto; }}
  .prow {{ display:block; width:100%; text-align:left; border:none; background:none; cursor:pointer;
           padding:10px 14px; border-bottom:1px solid var(--line); font:inherit; }}
  .prow:hover {{ background:#f4f4f4; }}
  .prow.active {{ background:var(--sel); color:var(--selink); }}
  .prow .pname {{ font-weight:600; font-size:14px; display:block; }}
  .prow .pmeta {{ font-size:12px; color:var(--mut); }}
  .prow.active .pmeta {{ color:#bbb; }}
  .dead {{ color:#b3261e; font-weight:700; }}
  .prow.active .dead {{ color:#ff8a80; }}
  .panel {{ border:1px solid var(--line); border-radius:8px; overflow:hidden; background:var(--bg); }}
  .panel-head {{ padding:14px 18px; border-bottom:1px solid var(--line); }}
  .panel-head h2 {{ margin:0 0 2px; font-size:19px; }}
  .panel-head .ftype {{ font-size:12px; color:var(--mut); margin-left:8px; font-weight:400; }}
  .panel-head .purl {{ font-size:13px; color:var(--mut); }}
  .panel-head .pnotes {{ font-size:13.5px; color:var(--ink); margin-top:6px; max-width:900px; }}
  .table-wrap {{ overflow-x:auto; }}
  table {{ border-collapse:collapse; width:100%; min-width:720px; font-size:13.5px; }}
  th {{ text-align:left; padding:9px 12px; cursor:pointer; white-space:nowrap; user-select:none;
       border-bottom:1px solid var(--line); font-size:12px; text-transform:uppercase;
       letter-spacing:.03em; color:var(--mut); }}
  th:hover {{ color:var(--ink); }}
  td {{ border-bottom:1px solid var(--line); padding:8px 12px; vertical-align:top; }}
  tr:last-child td {{ border-bottom:none; }}
  tr:hover td {{ background:#f7f7f7; }}
  td:first-child {{ font-weight:600; }}
  .empty {{ padding:40px 20px; text-align:center; color:var(--mut); }}
  .ftchips {{ border-top:1px solid var(--line); padding:12px 18px; font-size:13px; color:var(--mut); }}
  #about {{ position:fixed; inset:0; background:rgba(0,0,0,.35); display:none; align-items:center;
            justify-content:center; z-index:10; }}
  #about.open {{ display:flex; }}
  .modal {{ background:var(--bg); max-width:640px; width:92%; max-height:82vh; overflow-y:auto;
            padding:26px 28px; border-radius:10px; }}
  .modal h2 {{ margin:0 0 10px; font-size:18px; }}
  .modal p, .modal li {{ font-size:14px; color:var(--ink); }}
  .modal .x {{ position:absolute; }};
  .close {{ float:right; border:1px solid var(--line); background:none; font:inherit; font-size:14px;
            cursor:pointer; padding:2px 10px; border-radius:6px; }}
  footer {{ margin-top:32px; color:var(--mut); font-size:13px; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{html.escape(TITLE)}</h1>
    <p class="tagline">{tagline}</p>
    <span class="meta">verified {verified} · <a href="#about" id="aboutlink">about / contribute</a></span>
  </header>

  <noscript>
    <div class="table-wrap">
      <table><thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table>
    </div>
  </noscript>

  <div id="app" class="layout"></div>

  <footer>Numbers cross-checked against official docs and third-party trackers as of {verified}. Limits
  change without notice — this is a map, not a contract.</footer>
</div>

<div id="about" role="dialog" aria-modal="true">
  <div class="modal">
    <button class="close">close</button>
    <h2>About {html.escape(TITLE)}</h2>
    <p><strong>What is here:</strong> every provider that gives developers free API access to LLM
    inference — callable from a harness, agent, or CLI. Web-chat-only free tiers (ChatGPT, Claude.ai,
    Gemini app, deepseek.com, Grok, Copilot) are excluded on purpose.</p>
    <p><strong>What counts as free:</strong> API-accessible, strictly $0, no credit card required.
    Four shapes: rate-limited free (forever, throttled), promo free (limited time), free gateways
    (OpenRouter, OpenCode Zen), trial credits (one-time, expires — flagged in the model cost column).</p>
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
        <span class="pmeta">${{p.free_type}} · ${{p.models.length}} free models</span></button>`;
    }}).join("");
    providersEl.querySelectorAll(".prow").forEach(b =>
      b.addEventListener("click", () => {{ activeIdx = list.indexOf(rows[+b.dataset.i]); drawPanel(); drawSidebar(); }}));
    if (!rows.length) providersEl.innerHTML = `<div class="empty">No match.</div>`;
  }}

  function drawPanel() {{
    const p = list[activeIdx];
    const dead = p.dead ? `<div class="pnotes"><strong class="dead">Probe flags this provider unreachable — verify before relying on it.</strong></div>` : "";
    panel.innerHTML = `<div class="panel-head">
      <h2>${{p.name}}<span class="ftype">${{p.free_type}}</span></h2>
      <a class="purl" href="${{p.url}}" target="_blank" rel="noopener">${{p.url}}</a>
      <div class="pnotes">${{p.notes}}</div>
      <div class="pnotes"><strong>${{p.verified_method === "live-probe" ? "Live-probed" : "Docs-verified"}} ${{p.verified}}</strong>${{p.verified_method === "docs" ? " · no public API to probe; dates refresh on human verification pass" : " · re-verified nightly"}}</div>${{dead}}
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


def build_index_md():
    site = WEBSITE.rstrip("/")
    md = build_readme()
    for rel in ("data/providers.json", "CONTRIBUTING.md"):
        md = md.replace(f"]({rel})", f"]({site}/{rel})")
    return md


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
    (dist / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{WEBSITE}/</loc><lastmod>{VERIFIED}</lastmod></url>\n"
        "</urlset>\n"
    )
    (dist / "data" / "providers.json").write_text(json.dumps(DATA, indent=2) + "\n")
    (dist / "data" / "schema.json").write_text(json.dumps(build_schema(), indent=2) + "\n")
    # ponytail: per-provider JSON split; whole file is ~40KB so single-file fetch stays the default path
    for p in ROWS:
        (dist / "data" / f"{slug(p['name'])}.json").write_text(json.dumps(p, indent=2) + "\n")
    ai_bots = ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
               "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot", "Amazonbot")
    (dist / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n"
        + "".join(f"User-agent: {b}\nAllow: /\n" for b in ai_bots)
        + f"Sitemap: {WEBSITE}/sitemap.xml\n"
    )
    total = sum(len(p["models"]) for p in ROWS)
    print(f"ok: {len(ROWS)} providers, {total} models -> dist/ (verified {VERIFIED})")


if __name__ == "__main__":
    main()