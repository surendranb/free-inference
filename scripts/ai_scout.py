#!/usr/bin/env python3
"""Autonomous AI Studio Discovery Scout & Catalog Auditor for FreeInference.dev.

Runs nightly via GitHub Actions (.github/workflows/nightly-probe.yml) or locally.
1. Audits existing providers for staleness (>30 days), cost syntax errors, and missing base URLs.
2. Polls live model inventories across multiple aggregators (OpenRouter, Kilo, Nous, Requesty).
3. Uses Google AI Studio (gemini-3.5-flash-lite) to classify newly discovered free models.
4. Autonomously audits official documentation for stale/bundled providers, confirming active status
   and refreshing verified timestamps.
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from probe import gemini_key, get_json, _live_free_ids, UA

DATA_PATH = ROOT / "data" / "providers.json"
REPORT_PATH = ROOT / "data" / "scout_report.json"
MODEL_NAME = "gemini-3.5-flash-lite"
ANTIGRAVITY_AGENT = "antigravity-preview-09-2026"
INTERACTIONS_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"


def call_antigravity_agent(prompt, key, timeout=120):
    """Invoke Antigravity Managed Agent in Google's cloud sandbox with Chrome & web access."""
    url = f"{INTERACTIONS_URL}?key={key}"
    body = {
        "agent": ANTIGRAVITY_AGENT,
        "input": prompt,
        "environment": "remote",
        "background": True,
        "store": True,
        "agent_config": {
            "type": "antigravity",
            "max_total_tokens": 50000
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        init_res = json.load(r)
    
    iid = init_res.get("id")
    if not iid:
        raise RuntimeError("No interaction ID returned by Antigravity Agent API")
    
    poll_url = f"{INTERACTIONS_URL}/{iid}?key={key}"
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(5)
        with urllib.request.urlopen(poll_url, timeout=30) as r:
            poll_res = json.load(r)
        status = poll_res.get("status")
        if status in ("completed", "failed", "incomplete"):
            steps = poll_res.get("steps", [])
            output_text = ""
            for s in reversed(steps):
                for c in s.get("content", []):
                    if "text" in c and c["text"].strip():
                        output_text = c["text"].strip()
                        break
                if output_text:
                    break
            return {
                "status": status,
                "output_text": output_text,
                "steps_count": len(steps),
                "interaction_id": iid,
                "usage": poll_res.get("usage", {})
            }
    raise TimeoutError(f"Antigravity agent interaction {iid} timed out after {timeout}s")


def call_ai_studio(prompt, key, retries=1):
    """Call Google AI Studio gemini-3.5-flash-lite with retry."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={key}"
    req_body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(req_body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                res = json.load(r)
                return res["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"AI Studio call failed after retries: {e}")


def clean_html(html_str):
    """Strip scripts, styles, tags, and normalize whitespace."""
    s = re.sub(r'<(script|style|svg|noscript|head)[^>]*>.*?</\1>', ' ', html_str, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def extract_pricing_context(text, max_len=3000):
    """Extract relevant pricing and free-tier sentences to fit LLM prompt."""
    keywords = ["free", "pricing", "plan", "token", "credit", "rate limit", "allowance", "model", "tier", "quota"]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    matched = [s for s in sentences if any(kw in s.lower() for kw in keywords)]
    snippet = " ".join(matched)
    if len(snippet) < 300:
        snippet = text[:max_len]
    return snippet[:max_len]


def scout_openrouter_free_models():
    """Fetch all :free models from OpenRouter."""
    try:
        d = get_json("https://openrouter.ai/api/v1/models")
        free_models = []
        for m in d.get("data", []):
            mid = m.get("id", "")
            if ":free" in mid:
                free_models.append({
                    "id": mid,
                    "name": m.get("name", mid),
                    "context_length": m.get("context_length", 0),
                    "source": "OpenRouter"
                })
        return free_models
    except Exception as e:
        print(f"Warning: could not fetch OpenRouter models: {e}")
        return []


def poll_openrouter_rss(existing_models):
    """Directly poll OpenRouter RSS feed for new model additions with (free) tag."""
    url = "https://openrouter.ai/api/v1/models?use_rss=true"
    req = urllib.request.Request(url, headers={"User-Agent": "FreeInference-Scout/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            xml_data = r.read()
    except Exception as e:
        print(f"Notice: OpenRouter RSS fetch skipped: {e}")
        return []

    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"Notice: OpenRouter RSS parse failed: {e}")
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    catalog_ids = {m.lower().split("/")[-1].replace(":free", "") for m in existing_models}
    rss_discoveries = []
    for item in channel.findall("item"):
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
        desc = item.find("description").text if item.find("description") is not None else ""

        if "(free)" in title.lower() or ":free" in title.lower():
            id_match = re.search(r"\(([^()]+/[^()]+)\)", title)
            model_id = id_match.group(1).strip() if id_match else link.replace("https://openrouter.ai/", "").strip()
            base_id = model_id.split("/")[-1].replace(":free", "").lower()
            is_new = base_id not in catalog_ids and model_id.lower() not in {m.lower() for m in existing_models}
            rss_discoveries.append({
                "model_id": model_id,
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "description": desc[:200],
                "is_new_to_catalog": is_new
            })

    return rss_discoveries


def scout_endpoint_models(name, url):
    """Fetch all $0 / free models from a zero-price gateway endpoint."""
    try:
        d = get_json(url)
        items = d.get("data", d) if isinstance(d, dict) else d
        if not isinstance(items, list):
            return []
        free_ids = _live_free_ids(items)
        out = []
        for m in items:
            if isinstance(m, dict) and m.get("id") in free_ids:
                out.append({
                    "id": m.get("id"),
                    "name": m.get("name", m.get("id")),
                    "context_length": m.get("context_length", 0),
                    "source": name
                })
        return out
    except Exception as e:
        print(f"Warning: could not fetch {name} models: {e}")
        return []


def audit_catalog(catalog_data):
    """Perform ground truth audit on providers and models."""
    issues = []
    stale_providers = []
    today = date.today()

    for p in catalog_data.get("providers", []):
        pname = p.get("name", "Unknown")
        # Staleness check (>30 days)
        v_str = p.get("verified", "")
        try:
            v_date = datetime.fromisoformat(v_str).date()
            days_old = (today - v_date).days
            if days_old > 30:
                stale_providers.append({
                    "provider": pname,
                    "days_stale": days_old,
                    "verified": v_str,
                    "docs_url": p.get("docs_url") or p.get("url")
                })
        except ValueError:
            issues.append(f"{pname}: missing or invalid verified date '{v_str}'")

        # Base URL check on API providers
        if p.get("access_method") == "api_key" and not p.get("base_url"):
            issues.append(f"{pname}: API provider missing base_url")

        # Cost syntax check
        for m in p.get("models", []):
            cost = m.get("cost", "")
            if cost and not (cost.startswith("$") or "free" in cost.lower() or "0" in cost):
                issues.append(f"{pname} / {m.get('name')}: suspicious cost '{cost}'")

    return {
        "stale_count": len(stale_providers),
        "stale_providers": stale_providers,
        "syntax_issues": issues
    }


def audit_stale_provider_docs(catalog_data, key, apply_updates=False, max_audits=10):
    """Autonomously audit stale providers using Google AI Studio Antigravity Managed Agent in cloud sandbox."""
    today = date.today().isoformat()
    audit_results = []
    audited_count = 0

    for p in catalog_data.get("providers", []):
        if audited_count >= max_audits:
            break

        v_str = p.get("verified", "")
        try:
            v_date = datetime.fromisoformat(v_str).date()
            days_old = (date.today() - v_date).days
            if days_old <= 30:
                continue
        except ValueError:
            continue

        pname = p.get("name")
        doc_url = p.get("docs_url") or p.get("url")
        if not doc_url:
            continue

        print(f"--> [Antigravity Agent] Auditing live ground truth for {pname} ({doc_url})...")
        try:
            prompt = f"""You are the Antigravity ground truth auditor for FreeInference.dev.
Audit the official free tier for provider: {pname}.
Official Documentation / Pricing URL: {doc_url}

Current catalog data:
- Free tier type: {p.get('free_type')}
- Access method: {p.get('access_method')}
- Cataloged models: {[m.get('name') for m in p.get('models', [])]}

Task:
1. Navigate to {doc_url} using your tools (Google Chrome / url_context / curl / bash).
2. Inspect the live rendered page, pricing tables, quotas, token limits, and free allowances.
3. If the page redirected or pricing moved to a subpage, find the current pricing/free tier.
4. Output your conclusion strictly as a JSON object with keys:
- "status": "active" (free tier exists), "retired" (discontinued/paid-only), or "changed"
- "is_free_active": boolean
- "summary": concise 1-sentence summary of the verified free allowance, limits, and reset cadence.

Output valid JSON only with no conversational text.
"""
            agent_res = call_antigravity_agent(prompt, key, timeout=150)
            raw_out = agent_res.get("output_text", "")
            
            # Extract JSON block
            json_match = re.search(r'\{[^{}]*"status"[^{}]*\}', raw_out, re.DOTALL)
            if json_match:
                eval_data = json.loads(json_match.group(0))
            else:
                eval_data = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_out, flags=re.MULTILINE).strip())

            audit_entry = {
                "provider": pname,
                "docs_url": doc_url,
                "status": eval_data.get("status", "active"),
                "is_free_active": eval_data.get("is_free_active", True),
                "summary": eval_data.get("summary", ""),
                "audited_date": today,
                "agent_steps": agent_res.get("steps_count", 0),
                "interaction_id": agent_res.get("interaction_id")
            }
            audit_results.append(audit_entry)
            audited_count += 1

            if eval_data.get("is_free_active") and apply_updates:
                p["verified"] = today
                for m in p.get("models", []):
                    m["verified"] = today
                print(f"  ✓ Verified active ({agent_res.get('steps_count', 0)} agent steps): refreshed {pname} verification date to {today}.")
            elif not eval_data.get("is_free_active"):
                print(f"  ⚠ WARNING: Agent flagged {pname} as NOT active/free: {eval_data.get('summary')}")

        except Exception as e:
            print(f"  Notice: Antigravity agent audit skipped for {pname}: {e}")
            audit_results.append({
                "provider": pname,
                "docs_url": doc_url,
                "status": "unreachable",
                "is_free_active": None,
                "summary": str(e),
                "audited_date": today
            })

    return audit_results


def run_scout(apply_updates=False):
    print("--> Starting AI Studio Discovery Scout & Catalog Auditor...")
    today = date.today().isoformat()
    key = gemini_key()
    
    if not key:
        print("Skipped: No GEMINI_API_KEY available.")
        return 0

    catalog_data = json.loads(DATA_PATH.read_text())
    existing_models = {
        m["name"]: p["name"]
        for p in catalog_data["providers"]
        for m in p["models"]
    }

    # 1. Run Catalog Ground Truth Audit
    audit_summary = audit_catalog(catalog_data)
    print(f"Catalog status: {len(catalog_data['providers'])} providers, {len(existing_models)} models.")
    print(f"Stale providers (>30d): {audit_summary['stale_count']}")

    # 2. Multi-Source Discovery Scout across 4 gateways
    live_models = []
    live_models.extend(scout_openrouter_free_models())
    live_models.extend(scout_endpoint_models("Kilo Gateway", "https://api.kilo.ai/api/gateway/models"))
    live_models.extend(scout_endpoint_models("Nous Portal", "https://inference-api.nousresearch.com/v1/models"))
    live_models.extend(scout_endpoint_models("Requesty", "https://router.requesty.ai/v1/models"))

    new_discoveries = [m for m in live_models if m["id"] not in existing_models]
    print(f"Discovered {len(live_models)} live free models across 4 gateways ({len(new_discoveries)} new).")

    # 2b. Direct OpenRouter RSS Feed Stream for Real-Time Additions
    rss_free_models = poll_openrouter_rss(existing_models)
    new_rss_models = [m for m in rss_free_models if m.get("is_new_to_catalog")]
    print(f"OpenRouter RSS Stream: {len(rss_free_models)} free models found in feed ({len(new_rss_models)} new to catalog).")

    classified_candidates = []
    if new_discoveries:
        sample_to_classify = new_discoveries[:10]  # analyze top candidates
        prompt = f"""You are the automated catalog classifier for FreeInference.dev.
Analyze these newly discovered free LLM models from public gateways:
{json.dumps(sample_to_classify, indent=2)}

For each model, classify its architecture family, task category (coding, vision, reasoning, general), and whether it qualifies for free developer inference ($0 API).
Return a JSON array of objects with keys: "id", "family", "task", "recommended_page_slug", "summary".
Output strictly valid JSON with no markdown formatting.
"""
        try:
            raw_response = call_ai_studio(prompt, key)
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_response, flags=re.MULTILINE).strip()
            classified_candidates = json.loads(cleaned)
            print(f"Successfully classified {len(classified_candidates)} candidate models via AI Studio.")
        except Exception as e:
            print(f"AI classification notice: {e}")
            classified_candidates = [
                {"id": m["id"], "family": "unknown", "task": "general", "recommended_page_slug": "free-llm-api", "summary": m.get("name", "")}
                for m in sample_to_classify
            ]

    # 3. Autonomous Doc-Auditor for Stale Providers
    doc_audits = audit_stale_provider_docs(catalog_data, key, apply_updates=apply_updates, max_audits=18)
    print(f"Completed {len(doc_audits)} autonomous doc-audits.")

    if apply_updates and doc_audits:
        DATA_PATH.write_text(json.dumps(catalog_data, indent=2) + "\n")
        print(f"Updated {DATA_PATH} with fresh verification timestamps.")

    # Build report
    report = {
        "scouted_date": today,
        "model_used": f"{MODEL_NAME} + {ANTIGRAVITY_AGENT}",
        "providers_audited": len(catalog_data["providers"]),
        "models_cataloged": len(existing_models),
        "audit_summary": audit_summary,
        "doc_audits": doc_audits,
        "live_gateway_free_total": len(live_models),
        "new_discoveries_count": len(new_discoveries),
        "openrouter_rss_stream_count": len(rss_free_models),
        "openrouter_rss_new_count": len(new_rss_models),
        "openrouter_rss_stream": rss_free_models,
        "candidates": classified_candidates,
        "status": "completed"
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Scout report written to {REPORT_PATH}")

    # Emit GitHub Actions Step Summary if running in CI
    gh_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if gh_summary_path:
        with open(gh_summary_path, "a") as f:
            f.write(f"### 🤖 FreeInference Nightly AI Scout & Audit ({today})\n\n")
            f.write(f"- **Engines**: Discovery via `{MODEL_NAME}` · Live Sandbox Audits via `{ANTIGRAVITY_AGENT}`\n")
            f.write(f"- **Catalog Size**: {len(catalog_data['providers'])} providers · {len(existing_models)} models\n")
            f.write(f"- **Doc Audits Conducted**: {len(doc_audits)}\n")
            f.write(f"- **Live Gateway Models**: {len(live_models)} across 4 endpoints\n\n")
            if doc_audits:
                f.write("#### Autonomous Doc Audits\n\n")
                f.write("| Provider | Status | Summary |\n")
                f.write("| --- | --- | --- |\n")
                for d in doc_audits:
                    status_icon = "✓" if d.get("is_free_active") else "⚠"
                    f.write(f"| {d['provider']} | {status_icon} {d['status']} | {d['summary']} |\n")
                f.write("\n")
            if classified_candidates:
                f.write("#### Newly Discovered Candidate Models\n\n")
                f.write("| Model ID | Family | Task | Recommended Slug |\n")
                f.write("| --- | --- | --- | --- |\n")
                for c in classified_candidates:
                    f.write(f"| `{c.get('id')}` | {c.get('family')} | {c.get('task')} | `{c.get('recommended_page_slug')}` |\n")

    return 0


if __name__ == "__main__":
    apply_flag = "--apply" in sys.argv
    sys.exit(run_scout(apply_updates=apply_flag))
