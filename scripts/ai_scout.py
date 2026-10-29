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
    """Autonomously fetch documentation for stale providers and verify with AI Studio."""
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

        print(f"--> Auditing docs for {pname} ({doc_url})...")
        try:
            req = urllib.request.Request(doc_url, headers=UA)
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw_html = resp.read().decode('utf-8', errors='ignore')
            
            clean_text = clean_html(raw_html)
            snippet = extract_pricing_context(clean_text)

            prompt = f"""You are the automated ground truth auditor for FreeInference.dev.
Review this official documentation text for {pname}:
\"\"\"{snippet}\"\"\"

Current cataloged status for {pname}:
- Free tier type: {p.get('free_type')}
- Access method: {p.get('access_method')}
- Cataloged models: {[m.get('name') for m in p.get('models', [])]}

Answer strictly in JSON with keys:
- "status": "active" (if free tier/allowance still exists), "retired" (if shutdown/paid-only), or "changed"
- "is_free_active": boolean
- "summary": one sentence describing the verified free offering.

Output strictly valid JSON with no markdown fences.
"""
            ai_raw = call_ai_studio(prompt, key)
            ai_clean = re.sub(r"^```(?:json)?\s*|\s*```$", "", ai_raw, flags=re.MULTILINE).strip()
            eval_data = json.loads(ai_clean)

            audit_entry = {
                "provider": pname,
                "docs_url": doc_url,
                "status": eval_data.get("status", "active"),
                "is_free_active": eval_data.get("is_free_active", True),
                "summary": eval_data.get("summary", ""),
                "audited_date": today
            }
            audit_results.append(audit_entry)
            audited_count += 1

            if eval_data.get("is_free_active") and apply_updates:
                p["verified"] = today
                for m in p.get("models", []):
                    m["verified"] = today
                print(f"  ✓ Verified active: refreshed {pname} verification date to {today}.")
            elif not eval_data.get("is_free_active"):
                print(f"  ⚠ WARNING: AI flagged {pname} as NOT active/free: {eval_data.get('summary')}")

        except Exception as e:
            print(f"  Notice: doc audit skipped for {pname}: {e}")
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
        "model_used": MODEL_NAME,
        "providers_audited": len(catalog_data["providers"]),
        "models_cataloged": len(existing_models),
        "audit_summary": audit_summary,
        "doc_audits": doc_audits,
        "live_gateway_free_total": len(live_models),
        "new_discoveries_count": len(new_discoveries),
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
            f.write(f"- **Engine**: Google AI Studio `{MODEL_NAME}`\n")
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
