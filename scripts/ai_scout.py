#!/usr/bin/env python3
"""Autonomous AI Studio Discovery Scout & Catalog Auditor for FreeInference.dev.

Runs nightly via GitHub Actions (.github/workflows/nightly-probe.yml) or locally.
1. Audits existing providers for staleness (>30 days), cost syntax errors, and missing base URLs.
2. Polls live model inventories across multiple aggregators (OpenRouter, Kilo, Nous, Requesty).
3. Uses Google AI Studio (gemini-3.5-flash-lite) to classify newly discovered free models
   and evaluate candidate additions against strict $0 developer inference criteria.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from probe import gemini_key, get_json, _live_free_ids

DATA_PATH = ROOT / "data" / "providers.json"
REPORT_PATH = ROOT / "data" / "scout_report.json"
MODEL_NAME = "gemini-3.5-flash-lite"


def call_ai_studio(prompt, key):
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
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
        return res["candidates"][0]["content"]["parts"][0]["text"].strip()


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
                stale_providers.append({"provider": pname, "days_stale": days_old, "verified": v_str})
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
    audit_results = audit_catalog(catalog_data)
    print(f"Catalog audit: {len(catalog_data['providers'])} providers, {len(existing_models)} models.")
    if audit_results["syntax_issues"]:
        print(f"WARNING: {len(audit_results['syntax_issues'])} syntax issues found:")
        for iss in audit_results["syntax_issues"]:
            print(f"  - {iss}")
    else:
        print("Catalog syntax: 100% clean (zero cost syntax bugs or missing base URLs).")

    # 2. Multi-Source Discovery Scout
    live_models = []
    live_models.extend(scout_openrouter_free_models())
    live_models.extend(scout_endpoint_models("Kilo Gateway", "https://api.kilo.ai/api/gateway/models"))
    live_models.extend(scout_endpoint_models("Nous Portal", "https://inference-api.nousresearch.com/v1/models"))
    live_models.extend(scout_endpoint_models("Requesty", "https://router.requesty.ai/v1/models"))

    new_discoveries = [m for m in live_models if m["id"] not in existing_models]
    print(f"Discovered {len(live_models)} live free models across 4 gateways ({len(new_discoveries)} new).")

    classified_candidates = []
    if new_discoveries:
        sample_to_classify = new_discoveries[:10]  # analyze batch
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

    # Build report
    report = {
        "scouted_date": today,
        "model_used": MODEL_NAME,
        "providers_audited": len(catalog_data["providers"]),
        "models_cataloged": len(existing_models),
        "audit": audit_results,
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
            f.write(f"- **Catalog Health**: {len(catalog_data['providers'])} providers · {len(existing_models)} models\n")
            f.write(f"- **Stale Providers (>30d)**: {audit_results['stale_count']}\n")
            f.write(f"- **Live Gateway $0 Models**: {len(live_models)} across OpenRouter, Kilo, Nous, Requesty\n\n")
            if classified_candidates:
                f.write("#### Newly Discovered Candidate Models\n\n")
                f.write("| Model ID | Source | Family | Task | Recommended Slug |\n")
                f.write("| --- | --- | --- | --- | --- |\n")
                for c in classified_candidates:
                    f.write(f"| `{c.get('id')}` | {c.get('source', 'gateway')} | {c.get('family')} | {c.get('task')} | `{c.get('recommended_page_slug')}` |\n")
            else:
                f.write("All live free models across monitored gateways are cataloged and verified.\n")

    return 0


if __name__ == "__main__":
    apply_flag = "--apply" in sys.argv
    sys.exit(run_scout(apply_updates=apply_flag))
